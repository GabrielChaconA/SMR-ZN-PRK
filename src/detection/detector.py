import cv2
import numpy as np
from ultralytics import YOLO
from typing import Tuple

class ParkingDetector:
    """
    Clase backend que utiliza Ultralytics YOLOv8
    para detectar vehículos (coches, autobuses, camiones) con alta precisión.
    """
    
    def __init__(self):
        # Cargar el modelo preentrenado más ligero de YOLOv8
        # En el primer uso, descargará automáticamente el archivo yolov8n.pt (pocos MB)
        self.model = YOLO("yolov8n.pt")
        
        # Clases de COCO que nos interesan: 2: car, 5: bus, 7: truck
        self.target_classes = [2, 5, 7]
        print("ParkingDetector inicializado con Ultralytics YOLOv8.")

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, int]:
        """
        Detecta vehículos usando YOLO, dibuja Bounding Boxes sobre el frame original
        y lo devuelve en formato RGB junto con la cantidad de vehículos detectados.
        """
        # Ejecutar inferencia sobre el frame
        # verbose=False para no saturar los logs
        # conf=0.3 para filtrar falsos positivos de baja confianza
        results = self.model(frame, classes=self.target_classes, conf=0.3, verbose=False)
        
        processed_frame = frame.copy()
        detected_count = 0
        
        # Extraer las cajas delimitadoras del primer (y único) resultado
        for box in results[0].boxes:
            # Obtener coordenadas de la caja
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            
            # Dibujar rectángulo azul cyan
            cv2.rectangle(processed_frame, (x1, y1), (x2, y2), (255, 150, 0), 2)
            
            # Etiqueta
            label = f"{self.model.names[cls_id]} {conf:.2f}"
            cv2.putText(processed_frame, label, (x1, max(y1 - 10, 0)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 150, 0), 2)
                        
            detected_count += 1
                
        # Streamlit espera formato RGB
        return cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB), detected_count

