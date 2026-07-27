import streamlit as st
import cv2
import tempfile
import os
import sys

# Añadir raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.detection.space_finder import SpaceFinder

st.set_page_config(
    page_title="CAM SCAN — Control Room",
    page_icon="📹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS Personalizado para un look de "Centro de Control" ──────────────────
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #e2e8f0;
    }
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: -1rem;
    }
    .sub-header {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
    .metric-box {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #334155;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-title {
        font-size: 0.8rem;
        text-transform: uppercase;
        color: #94a3b8;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #f8fafc;
    }
    .metric-blue { color: #60a5fa; }
    .metric-green { color: #4ade80; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_detector():
    return SpaceFinder()

def draw_metric_box(title, value, color_class=""):
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">{title}</div>
        <div class="metric-value {color_class}">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def main():
    st.markdown('<div class="main-header">📷 CAM SCAN Control Room</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Búsqueda de Huecos en Calle (Universal AI)</div>', unsafe_allow_html=True)

    detector = load_detector()

    # ── Layout ───────────────────────────────────────────────
    col_sidebar, col_feed = st.columns([1, 3])

    with col_sidebar:
        st.subheader("Configuración de Fuente")
        uploaded_file = st.file_uploader(
            "Cargar metraje CCTV (Video/Imagen)",
            type=["mp4", "avi", "mov", "jpg", "jpeg", "png"]
        )
        btn_process = st.button("▶ Iniciar Monitoreo", type="primary", use_container_width=True)
        
        st.divider()
        st.subheader("Analíticas en Vivo")
        
        # Placeholders para las métricas que se actualizarán en el bucle
        metric_cars_placeholder = st.empty()
        metric_free_placeholder = st.empty()
        
        # Valores por defecto
        with metric_cars_placeholder.container():
            draw_metric_box("Vehículos Detectados", 0, "metric-blue")
        with metric_free_placeholder.container():
            draw_metric_box("Huecos Libres", 0, "metric-green")

    with col_feed:
        # Aquí se renderizará el video
        feed_placeholder = st.empty()
        
        if not btn_process:
            feed_placeholder.markdown("""
            <div style='background-color:#1e293b; aspect-ratio:16/9; display:flex; align-items:center; justify-content:center; border: 1px dashed #475569; border-radius:0.5rem;'>
                <span style='color:#64748b;'>Esperando señal de video...</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Lógica de procesamiento ───────────────────────────────────────────────
    if btn_process:
        if uploaded_file is None:
            # Usar video de referencia por defecto
            default_video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/raw/custom/videos/referencia estacionamiento.mp4'))
            if os.path.exists(default_video_path):
                st.info("Usando video de referencia por defecto...")
                source_path = default_video_path
                is_video = True
                tfile = None
            else:
                st.error("Por favor sube un archivo para procesar.")
                return
        else:
            suffix = os.path.splitext(uploaded_file.name)[-1].lower()
            is_video = suffix in [".mp4", ".avi", ".mov"]

            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tfile.write(uploaded_file.read())
            tfile.flush()
            source_path = tfile.name

        if is_video:
            cap = cv2.VideoCapture(source_path)
            if not cap.isOpened():
                st.error("Error al leer el video.")
                if tfile is not None:
                    tfile.close()
                    os.unlink(source_path)
                return

            with st.spinner("Ejecutando SpaceFinder..."):
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    processed_rgb, cars, valid_gaps = detector.process_frame(frame)

                    # Actualizar UI
                    with metric_cars_placeholder.container():
                        draw_metric_box("Vehículos Detectados", cars, "metric-blue")
                    with metric_free_placeholder.container():
                        draw_metric_box("Huecos Libres", valid_gaps, "metric-green")

                    feed_placeholder.image(processed_rgb, channels="RGB", use_container_width=True)

            cap.release()
            st.success("Transmisión finalizada.")

        else:
            # Imagen estática
            frame = cv2.imread(source_path)
            if frame is not None:
                processed_rgb, cars, valid_gaps = detector.process_frame(frame)
                
                with metric_cars_placeholder.container():
                    draw_metric_box("Vehículos Detectados", cars, "metric-blue")
                with metric_free_placeholder.container():
                    draw_metric_box("Huecos Libres", valid_gaps, "metric-green")
                    
                feed_placeholder.image(processed_rgb, channels="RGB", use_container_width=True)
                st.success("Análisis de imagen completado.")

        if tfile is not None:
            tfile.close()
            os.unlink(source_path)

if __name__ == "__main__":
    main()
