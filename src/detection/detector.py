import cv2
import numpy as np
from ultralytics import YOLO
from typing import Tuple

# Clases COCO relevantes por categoría
VEHICLE_CLASSES   = {2: "car", 5: "bus", 7: "truck", 3: "motorcycle"}
POLE_CLASSES      = {9: "traffic light", 11: "stop sign"}   # proxies de postes urbanos
# Árboles: COCO no tiene clase "tree". Se usa "potted plant" (58) como proxy visible
# y se complementará con detección por color/forma en el futuro.
PLANT_CLASSES     = {58: "plant"}

# Colores BGR para cada categoría
COLOR_VEHICLE = (255, 140, 0)   # Naranja
COLOR_POLE    = (0, 200, 255)   # Cyan
COLOR_PLANT   = (0, 200, 80)    # Verde


class ParkingDetector:
    """
    Clase backend que utiliza Ultralytics YOLOv8 para detectar:
      - Vehículos (carros, camiones, buses, motos)
      - Postes / señales de tráfico (proxy urbano)
      - Plantas / árboles (proxy; COCO no tiene clase 'tree')

    Devuelve el frame procesado más los conteos de cada categoría.
    """

    def __init__(self):
        self.model = YOLO("yolov8n.pt")
        # Unión de todas las clases que nos importan
        self.target_classes = list(
            VEHICLE_CLASSES.keys() | POLE_CLASSES.keys() | PLANT_CLASSES.keys()
        )
        print("ParkingDetector inicializado con Ultralytics YOLOv8.")

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, int, int, int]:
        """
        Detecta objetos relevantes usando YOLO, dibuja Bounding Boxes
        y devuelve:
          (frame_rgb, n_vehicles, n_poles, n_trees)
        """
        results = self.model(
            frame,
            classes=self.target_classes,
            conf=0.3,
            verbose=False
        )

        processed = frame.copy()
        n_vehicles = 0
        n_poles    = 0
        n_trees    = 0

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf   = float(box.conf[0])
            cls_id = int(box.cls[0])

            # Determinar categoría y color
            if cls_id in VEHICLE_CLASSES:
                color = COLOR_VEHICLE
                label_prefix = VEHICLE_CLASSES[cls_id]
                n_vehicles += 1
            elif cls_id in POLE_CLASSES:
                color = COLOR_POLE
                label_prefix = POLE_CLASSES[cls_id]
                n_poles += 1
            elif cls_id in PLANT_CLASSES:
                color = COLOR_PLANT
                label_prefix = PLANT_CLASSES[cls_id]
                n_trees += 1
            else:
                continue

            cv2.rectangle(processed, (x1, y1), (x2, y2), color, 2)
            label = f"{label_prefix} {conf:.2f}"
            cv2.putText(
                processed, label,
                (x1, max(y1 - 10, 0)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )

        return cv2.cvtColor(processed, cv2.COLOR_BGR2RGB), n_vehicles, n_poles, n_trees
