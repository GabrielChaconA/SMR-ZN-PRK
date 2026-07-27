import streamlit as st
import cv2
import tempfile
import os
import sys

# Añadir raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.detection.space_finder import SpaceFinder

st.set_page_config(
    page_title="SMART ZONE PARK - AI System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS Personalizado para un look de "Cine / Hollywood" ──────────────────
st.markdown("""
<style>
    /* Fondo completamente negro */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    /* Ajustar márgenes para que no se corte el texto superior */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 1rem !important;
        max-width: 95% !important;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 2px;
        margin-bottom: -0.5rem;
        text-transform: uppercase;
    }
    .sub-header {
        color: #0078D7; /* Azul corporativo que mostraste en el logo */
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 3px;
        margin-bottom: 1.5rem;
        text-transform: uppercase;
    }
    .metric-box {
        background-color: #0a0a0a;
        padding: 1.5rem 1rem;
        border-radius: 4px;
        border: 1px solid #222;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.5);
    }
    .metric-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        color: #888;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 3rem;
        font-weight: 300;
        color: #ffffff;
    }
    .metric-blue { color: #0078D7; }
    .metric-green { color: #00ff66; }
    
    /* Botones estilo minimalista */
    .stButton>button {
        border-radius: 2px !important;
        font-weight: bold;
        letter-spacing: 1px;
    }
    
    /* Evitar que videos verticales o muy grandes hagan la página infinita */
    [data-testid="stImage"] img {
        max-height: 75vh !important;
        object-fit: contain !important;
    }
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
    st.markdown('<div class="main-header">SMART ZONE PARK</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">SISTEMA DE ESTACIONAMIENTO CON IA</div>', unsafe_allow_html=True)

    detector = load_detector()

    # Estado de ejecución para arrancar y detener
    if "is_running" not in st.session_state:
        st.session_state.is_running = False

    # ── Layout ───────────────────────────────────────────────
    # Proporción 1 a 2.5 para que el video no se vuelva tan alto que se salga de la pantalla
    col_sidebar, col_feed = st.columns([1, 2.5])

    with col_sidebar:
        st.markdown("<div style='color:#888; font-size:0.8rem; letter-spacing:1px; margin-bottom:10px;'>PANEL DE CONTROL</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Fuente CCTV",
            type=["mp4", "avi", "mov", "jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        
        c1, c2 = st.columns(2)
        with c1:
            btn_start = st.button("INICIAR", type="primary", use_container_width=True)
        with c2:
            btn_stop = st.button("PARAR", type="secondary", use_container_width=True)
            
        if btn_start:
            st.session_state.is_running = True
        if btn_stop:
            st.session_state.is_running = False
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Placeholders para métricas
        metric_cars_placeholder = st.empty()
        metric_free_placeholder = st.empty()
        
        with metric_cars_placeholder.container():
            draw_metric_box("Vehículos", 0, "metric-blue")
        with metric_free_placeholder.container():
            draw_metric_box("Huecos Libres", 0, "metric-green")

    with col_feed:
        feed_placeholder = st.empty()
        
        if not st.session_state.is_running:
            feed_placeholder.markdown("""
            <div style='background-color:#050505; aspect-ratio:16/9; display:flex; align-items:center; justify-content:center; border: 1px solid #222;'>
                <span style='color:#333; font-family: monospace; letter-spacing: 2px;'>NO SIGNAL</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Lógica de procesamiento ───────────────────────────────────────────────
    if st.session_state.is_running:
        if uploaded_file is None:
            default_video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/raw/custom/videos/referencia estacionamiento.mp4'))
            if os.path.exists(default_video_path):
                source_path = default_video_path
                is_video = True
                tfile = None
            else:
                st.error("Error: No se encontró fuente de video.")
                st.session_state.is_running = False
                st.rerun()
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
                st.session_state.is_running = False
                st.rerun()

            while cap.isOpened() and st.session_state.is_running:
                ret, frame = cap.read()
                if not ret:
                    break

                processed_rgb, cars, valid_gaps = detector.process_frame(frame)

                with metric_cars_placeholder.container():
                    draw_metric_box("Vehículos", cars, "metric-blue")
                with metric_free_placeholder.container():
                    draw_metric_box("Huecos Libres", valid_gaps, "metric-green")

                # Mostrar imagen ajustada a la columna pero completa
                feed_placeholder.image(processed_rgb, channels="RGB", use_container_width=True)

            cap.release()
            if tfile is not None:
                tfile.close()
                os.unlink(source_path)
                
            # Si el video terminó naturalmente
            if not st.session_state.is_running:
                st.rerun()

        else:
            # Imagen estática
            frame = cv2.imread(source_path)
            if frame is not None:
                processed_rgb, cars, valid_gaps = detector.process_frame(frame)
                
                with metric_cars_placeholder.container():
                    draw_metric_box("Vehículos", cars, "metric-blue")
                with metric_free_placeholder.container():
                    draw_metric_box("Huecos Libres", valid_gaps, "metric-green")
                    
                feed_placeholder.image(processed_rgb, channels="RGB", use_container_width=True)

            if tfile is not None:
                tfile.close()
                os.unlink(source_path)
            
            st.session_state.is_running = False

if __name__ == "__main__":
    main()
