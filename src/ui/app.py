import streamlit as st
import cv2
import tempfile

# Importar el controlador del Backend
from src.detection.detector import ParkingDetector

# Configuración de página
st.set_page_config(page_title="Smart Parking ML", layout="wide")

# Inicialización limpia del backend (Se ejecuta una sola vez gracias a la caché)
@st.cache_resource
def load_detector():
    """
    Inicializa el modelo de Machine Learning y lo almacena en caché.
    Esto previene que Streamlit recargue la red neuronal pesada
    cada vez que el usuario hace un clic en la interfaz.
    """
    return ParkingDetector()

def main():
    st.title("Sistema Inteligente de Detección de Estacionamiento")
    st.write("Interfaz de usuario conectada al Backend (Monolito Modular).")
    
    # 1. Cargar el backend (ML)
    detector = load_detector()
    
    st.success(f"✅ Backend de ML conectado exitosamente. Ejecutando en: **{detector.device}**")

    # 2. Interfaz de subida de video
    st.subheader("Prueba de Lectura y Detección")
    st.info("Sube un video para pasarlo al backend y procesarlo frame por frame.")
    
    uploaded_video = st.file_uploader("Sube un video de prueba (mp4)", type=["mp4"])
    
    if uploaded_video is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        
        cap = cv2.VideoCapture(tfile.name)
        
        if not cap.isOpened():
            st.error("Error al intentar abrir el video.")
        else:
            stframe = st.empty() # Contenedor para el video
            
            if st.button("Ejecutar Backend (ML)"):
                with st.spinner("Procesando con ML..."):
                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break
                        
                        # 3. Delegar TODA la lógica de ML al backend
                        processed_rgb_frame = detector.process_frame(frame)
                        
                        # 4. Renderizar el resultado (Responsabilidad de la UI)
                        stframe.image(processed_rgb_frame, channels="RGB")
                        
                cap.release()
                st.success("Procesamiento de ML finalizado.")

if __name__ == "__main__":
    main()
