import streamlit as st
import cv2
import tempfile
import os

# Importar el controlador del Backend
from src.detection.detector import ParkingDetector

# Configuración de página
st.set_page_config(page_title="Smart Parking ML", layout="wide")

# Inicialización limpia del backend (Se ejecuta una sola vez gracias a la caché)
@st.cache_resource
def load_detector():
    """
    Inicializa el modelo de Machine Learning y lo almacena en caché.
    """
    return ParkingDetector()

def main():
    st.title("Sistema Inteligente de Detección de Estacionamiento")
    st.write("Demostración visual con OpenCV Background Subtraction (MOG2).")
    
    # 1. Cargar el backend (ML)
    detector = load_detector()
    
    st.success("✅ Motor de Detección (MOG2) inicializado correctamente.")

    # 2. Interfaz de Video
    st.subheader("Prueba de Lectura y Detección")
    
    # Intentar usar el video de muestra por defecto
    default_video_path = os.path.join("data", "raw", "custom", "videos", "sample_parking.mp4")
    
    # Opcional: Permitir al usuario subir su propio video
    uploaded_video = st.file_uploader("Opcional: Sube un video propio (mp4)", type=["mp4"])
    
    video_source = None
    if uploaded_video is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        video_source = tfile.name
    elif os.path.exists(default_video_path):
        video_source = default_video_path
        st.info(f"Utilizando video de muestra por defecto: `{default_video_path}`")
    else:
        st.warning("No se encontró el video de muestra y no has subido ninguno.")
        return
        
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        st.error("Error al intentar abrir el video.")
    else:
        # Layout Lado a Lado
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Procesado con OpenCV (Izquierda)")
            stframe_processed = st.empty()
            
        with col2:
            st.markdown("### Video Original (Derecha)")
            stframe_original = st.empty()
            
        if st.button("Ejecutar Análisis", type="primary"):
            with st.spinner("Analizando frames..."):
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # El frame original viene en BGR, lo pasamos a RGB para Streamlit
                    rgb_original = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Delegar lógica al backend (procesa y devuelve RGB)
                    processed_rgb_frame = detector.process_frame(frame)
                    
                    # Renderizar ambos resultados simultáneamente
                    stframe_processed.image(processed_rgb_frame, channels="RGB", use_container_width=True)
                    stframe_original.image(rgb_original, channels="RGB", use_container_width=True)
                    
            cap.release()
            st.success("Análisis finalizado.")

if __name__ == "__main__":
    main()

