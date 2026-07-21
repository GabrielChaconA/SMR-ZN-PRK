import streamlit as st
import cv2
import tempfile
import os
import sys
import base64

# Añadir la raíz del proyecto al sys.path para que encuentre la carpeta 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.detection.detector import ParkingDetector

# Configuración de página con título actualizado
st.set_page_config(page_title="Smart Zone Park", layout="wide")

@st.cache_resource
def load_detector():
    return ParkingDetector()

def get_base64_of_bin_file(bin_file):
    """Lee un archivo y lo convierte a base64 para inyectarlo en HTML."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

def render_html_sidebar(occupied_count: int, total_spots: int = 40):
    """Genera el HTML de las tarjetas laterales (Stats) con los números dinámicos de YOLO."""
    free_count = total_spots - occupied_count
    occupancy_pct = int((occupied_count / total_spots) * 100) if total_spots > 0 else 0
    
    html = f"""
    <div class="tech-card">
        <div class="stat-icon icon-blue"></div>
        <div class="stat-content">
            <span class="stat-label">Total de carros (Detectados)</span>
            <span class="stat-value">{occupied_count}</span>
        </div>
    </div>
    
    <div class="tech-card">
        <div class="stat-icon icon-red"></div>
        <div class="stat-content">
            <span class="stat-label">Espacios ocupados</span>
            <span class="stat-value">{occupied_count}</span>
        </div>
    </div>
    
    <div class="tech-card">
        <div class="stat-icon icon-green"></div>
        <div class="stat-content">
            <span class="stat-label">Espacios libres</span>
            <span class="stat-value">{free_count}</span>
        </div>
    </div>
    
    <div class="tech-card" style="flex-direction: column; align-items: flex-start; gap: 0.5rem;">
        <div style="display: flex; justify-content: space-between; width: 100%;">
            <span class="stat-label">Ocupación</span>
            <span class="stat-value" style="font-size: 1rem;">{occupancy_pct}%</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {occupancy_pct}%;"></div>
        </div>
        <span class="stat-label" style="font-size: 0.75rem; margin-top: 0.25rem;">
            {occupied_count} de {total_spots} espacios estimados ocupados
        </span>
    </div>
    """
    return html

def main():
    # 1. Inyectar CSS personalizado
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # 2. Renderizar Header Personalizado
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    logo_b64 = get_base64_of_bin_file(logo_path)
    
    st.markdown(f"""
    <div class="szp-header">
        <div class="szp-logo-box">
            <img src="data:image/png;base64,{logo_b64}" alt="Logo" style="height: 3.5rem;">
        </div>
        <div class="szp-title-box">
            <h1>Smart Zone Park</h1>
            <p>Sistema de estacionamiento con IA</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    detector = load_detector()

    # 3. Layout Principal (Grilla)
    col_main, col_sidebar = st.columns([7, 3])
    
    with col_main:
        col_title, col_btn = st.columns([6, 4])
        with col_title:
            st.markdown("""
            <h3 style="margin: 0; padding-top: 0.5rem; font-size: 1.1rem; display: flex; align-items: center; gap: 0.5rem; color: #f8fafc;">
                Vista del estacionamiento
            </h3>
            """, unsafe_allow_html=True)
        with col_btn:
            btn_start = st.button("Ejecutar Monitoreo", type="primary", use_container_width=True)
            
        stframe_processed = st.empty()
        
        # Mostrar el recuadro negro por defecto antes de correr el video
        stframe_processed.markdown("""
        <div class="video-placeholder">
            <p>Esperando entrada de video...</p>
        </div>
        """, unsafe_allow_html=True)

        # El file uploader va debajo de la pantalla de transmisión
        st.markdown("<h4 style='color:#94a3b8; font-size:0.85rem; text-transform:uppercase; margin-top:0.5rem; margin-bottom:0;'>Cargar multimedia local</h4>", unsafe_allow_html=True)
        uploaded_video = st.file_uploader("Agrega fotos o videos para procesarlos con IA", type=["mp4", "jpg", "png"], label_visibility="collapsed")
        
    with col_sidebar:
        # Contenedor dinámico para las estadísticas
        st_stats = st.empty()
        # Render inicial translúcido indicando espera
        st_stats.markdown("""
        <div class="sidebar-placeholder">
            Esperando entrada...
        </div>
        """, unsafe_allow_html=True)

    # Lógica de carga de archivo
    default_video_path = os.path.join("data", "raw", "custom", "videos", "bdd_sample.mp4")
    video_source = None
    if uploaded_video is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        video_source = tfile.name
    elif os.path.exists(default_video_path):
        video_source = default_video_path

    # 4. Loop de Procesamiento
    if btn_start:
        if not video_source:
            st.warning("Sube un video o foto para comenzar.")
            return

        cap = cv2.VideoCapture(video_source)
        if not cap.isOpened():
            st.error("Error abriendo el archivo.")
            return
            
        with st.spinner("Inicializando modelo YOLOv8..."):
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Procesar con YOLO
                processed_rgb, cars_count = detector.process_frame(frame)
                
                # Actualizar Video
                stframe_processed.image(processed_rgb, channels="RGB", use_container_width=True)
                
                # Reemplazar el placeholder con los stats reales
                st_stats.markdown(render_html_sidebar(cars_count), unsafe_allow_html=True)
                
        cap.release()
        st.success("Monitoreo finalizado.")

if __name__ == "__main__":
    main()

