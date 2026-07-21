import cv2
import torch
import numpy as np
# from ultralytics import YOLO

class ParkingDetector:
    """
    Clase backend que aísla la lógica de Machine Learning (YOLO, OpenCV, PyTorch).
    La interfaz de usuario de Streamlit se comunicará con esta clase, en lugar de 
    ejecutar inferencias o lógica de OpenCV directamente en el archivo UI.
    """
    
    def __init__(self):
        # Aquí se cargarían los pesos del modelo YOLO o cualquier otro modelo
        # Por ahora usaremos un mock simple para verificar la conectividad.
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._load_model()
        print(f"ParkingDetector inicializado usando dispositivo: {self.device}")

    def _load_model(self):
        """Simula la carga de un modelo pesado. Debe ejecutarse solo una vez."""
        # self.model = YOLO("yolov8n.pt")
        self.model_loaded = True
        
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Recibe un frame (imagen) BGR desde OpenCV, realiza la inferencia de ML,
        dibuja las predicciones (bounding boxes) y lo devuelve en formato RGB
        para que la UI de Streamlit lo renderice fácilmente.
        """
        if not self.model_loaded:
            raise RuntimeError("El modelo no ha sido cargado.")

        # SIMULACIÓN DE INFERENCIA: 
        # En el código real, aquí llamaríamos a self.model(frame) y 
        # procesaríamos las cajas de detección.
        
        # Simulamos procesamiento agregando texto sobre el frame
        processed_frame = frame.copy()
        
        # OpenCV usa BGR por defecto, escribimos texto en verde simulando detección
        cv2.putText(
            processed_frame, 
            f"Inferencia ML Activa (Dispositivo: {self.device})", 
            (20, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (0, 255, 0), # Verde en BGR
            2
        )
        
        # Streamlit espera imágenes en formato RGB, así que el backend se encarga 
        # de devolver la imagen en el formato adecuado para la Vista.
        rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        
        return rgb_frame
