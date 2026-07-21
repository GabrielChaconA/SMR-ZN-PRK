import cv2
import numpy as np

class ParkingDetector:
    """
    Clase backend que utiliza OpenCV Background Subtractor (MOG2)
    para detectar vehículos en movimiento sin requerir modelos pesados de Deep Learning.
    """
    
    def __init__(self):
        # MOG2 es robusto ante sombras y cambios de iluminación (ideal para estacionamientos)
        self.back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)
        # Filtro de tamaño mínimo para ignorar ruido (pájaros, hojas)
        self.min_area = 500
        print("ParkingDetector inicializado con OpenCV MOG2.")

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Detecta objetos en movimiento, dibuja Bounding Boxes sobre el frame original
        y lo devuelve en formato RGB para Streamlit.
        """
        # 1. Aplicar substracción de fondo para obtener la máscara
        fg_mask = self.back_sub.apply(frame)
        
        # 2. Limpiar el ruido de la máscara usando operaciones morfológicas
        # Kernel 5x5 para eliminar píxeles sueltos
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        
        # 3. Encontrar contornos de los objetos detectados
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        processed_frame = frame.copy()
        detected_count = 0
        
        # 4. Dibujar Bounding Boxes sobre los contornos grandes
        for contour in contours:
            if cv2.contourArea(contour) > self.min_area:
                x, y, w, h = cv2.boundingRect(contour)
                # Dibujar rectángulo ROJO (en BGR es 0, 0, 255)
                cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
                # Opcional: Escribir etiqueta arriba de la caja
                cv2.putText(processed_frame, "Movimiento", (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                detected_count += 1
                
        # 5. Agregar contador en la esquina
        cv2.putText(
            processed_frame, 
            f"Objetos detectados: {detected_count}", 
            (20, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (0, 255, 0), # Verde
            2
        )
        
        # Streamlit espera formato RGB
        return cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)

