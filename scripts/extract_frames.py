import cv2
import os
import argparse

def extract_frames(video_path, output_dir, frame_interval=30):
    """
    Extrae fotogramas de un video cada 'frame_interval' cuadros.
    Útil para generar datasets de entrenamiento.
    """
    if not os.path.exists(video_path):
        print(f"Error: No se encontró el video en {video_path}")
        return

    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: No se pudo abrir el archivo de video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video FPS: {fps}, Total de cuadros: {total_frames}")
    
    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Guardar 1 de cada 'frame_interval' cuadros
        if frame_count % frame_interval == 0:
            output_file = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(output_file, frame)
            saved_count += 1
            
        frame_count += 1

    cap.release()
    print(f"✅ Se extrajeron {saved_count} imágenes en '{output_dir}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae fotogramas de un video para Dataset YOLO.")
    parser.add_argument("--video", type=str, default="referencia/referencia estacionamiento.mp4", help="Ruta al video de origen")
    parser.add_argument("--output", type=str, default="data/raw/custom/frames", help="Carpeta destino para las imágenes")
    parser.add_argument("--interval", type=int, default=30, help="Intervalo de extracción (ej. 30 = extrae 1 de cada 30 cuadros)")
    
    args = parser.parse_args()
    
    extract_frames(args.video, args.output, args.interval)
