import cv2
import numpy as np
from ultralytics import YOLO
from typing import Tuple, List, Dict

# Constantes de Detección
VEHICLE_CLASSES = {2: "car", 5: "bus", 7: "truck"}

class SpaceFinder:
    """
    Motor de Inteligencia Artificial Universal para estacionamientos en la calle.
    Detecta vehículos, calcula perspectivas (Homografía) y mide espacios (Gaps).
    """

    def __init__(self):
        self.model = YOLO("yolov8n.pt")
        self.target_classes = list(VEHICLE_CLASSES.keys())
        
        # Parámetros por defecto para la Homografía (Vista de pájaro)
        # Se asume una resolución estándar de 1280x720 para el video de referencia
        self.src_pts = np.float32([
            [400, 300], [880, 300],  # Puntos superiores (al fondo de la calle)
            [1180, 700], [100, 700]  # Puntos inferiores (cerca de la cámara) - orden: BL, BR, TR, TL o algo similar
        ])
        
        # Mapeo a un rectángulo perfecto (Bird's Eye View)
        # 1 pixel = aprox 1 cm, entonces 500 px = 5 metros
        self.dst_pts = np.float32([
            [0, 0], [400, 0],
            [400, 800], [0, 800]
        ])
        
        self.matrix = cv2.getPerspectiveTransform(self.src_pts, self.dst_pts)
        
        # Distancia mínima para considerar un espacio válido (ej. 5 metros = 500 px virtuales)
        self.min_gap_distance_px = 500

    def get_bottom_center(self, box: List[int]) -> Tuple[int, int]:
        """Calcula el centro inferior de un bounding box (donde tocan las llantas)"""
        x1, y1, x2, y2 = box
        return (int((x1 + x2) / 2), y2)

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, int, int]:
        """
        Procesa el fotograma:
        1. Detecta vehículos
        2. Proyecta las posiciones a 2D (BEV)
        3. Encuentra huecos válidos
        """
        results = self.model(frame, classes=self.target_classes, conf=0.3, verbose=False)
        processed = frame.copy()
        
        # Extraer posiciones
        vehicles_pts_src = []
        boxes = []
        
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            
            # Dibujar vehículo en rojo oscuro
            cv2.rectangle(processed, (x1, y1), (x2, y2), (0, 0, 200), 2)
            
            # Punto de contacto con el suelo
            bottom_center = self.get_bottom_center([x1, y1, x2, y2])
            vehicles_pts_src.append(bottom_center)
            boxes.append([x1, y1, x2, y2])
            
            cv2.circle(processed, bottom_center, 6, (0, 165, 255), -1)

        # Si hay menos de 2 vehículos, no podemos medir huecos "entre" ellos
        if len(vehicles_pts_src) < 2:
            return cv2.cvtColor(processed, cv2.COLOR_BGR2RGB), len(vehicles_pts_src), 0

        # Transformar puntos al plano Bird's Eye View
        pts_np = np.array([vehicles_pts_src], dtype=np.float32)
        pts_bev = cv2.perspectiveTransform(pts_np, self.matrix)[0]

        # Ordenar los vehículos por su posición X en la vista original (de izquierda a derecha)
        # Esto asume que los autos están estacionados en paralelo a la acera
        sorted_indices = np.argsort([pt[0] for pt in vehicles_pts_src])
        
        valid_gaps = 0

        # Calcular distancia entre vehículos adyacentes
        for i in range(len(sorted_indices) - 1):
            idx_a = sorted_indices[i]
            idx_b = sorted_indices[i+1]
            
            pt_bev_a = pts_bev[idx_a]
            pt_bev_b = pts_bev[idx_b]
            
            # Distancia Euclidiana en el plano virtual 2D
            dist_bev = np.linalg.norm(pt_bev_a - pt_bev_b)
            
            # Puntos originales
            pt_src_a = vehicles_pts_src[idx_a]
            pt_src_b = vehicles_pts_src[idx_b]
            
            if dist_bev >= self.min_gap_distance_px:
                # ¡Es un hueco válido! Dibujar verde
                color = (0, 255, 0)
                valid_gaps += 1
                label = f"OK ({int(dist_bev)})"
            else:
                # Muy pequeño
                color = (0, 0, 255)
                label = f"No ({int(dist_bev)})"
                
            cv2.line(processed, pt_src_a, pt_src_b, color, 4)
            
            # Poner texto
            mid_pt = (int((pt_src_a[0] + pt_src_b[0])/2), int((pt_src_a[1] + pt_src_b[1])/2))
            cv2.putText(processed, label, (mid_pt[0]-20, mid_pt[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Dibujar polígono de calibración (Trapecio) semi-transparente para debug
        overlay = processed.copy()
        poly_pts = np.int32([self.src_pts[0], self.src_pts[1], self.src_pts[2], self.src_pts[3]])
        cv2.polylines(overlay, [poly_pts], isClosed=True, color=(255, 255, 0), thickness=2)
        cv2.addWeighted(overlay, 0.4, processed, 0.6, 0, processed)

        return cv2.cvtColor(processed, cv2.COLOR_BGR2RGB), len(vehicles_pts_src), valid_gaps
