import numpy as np
from typing import Tuple, Dict, Any
import os

from src.datasets.core.base_dataset import BaseDataset
from src.datasets.core.registry import register_dataset

@register_dataset("bdd100k")
class BDD100KDataset(BaseDataset):
    """
    Implementación concreta para leer el dataset oficial BDD100K.
    Responsabilidad (SRP): Parsear los archivos JSON de BDD100K y cargarlos en RAM a demanda.
    """
    
    def _load_index(self) -> None:
        # En la realidad, aquí abrirías el archivo JSON masivo (ej. bdd100k_labels_images_train.json)
        # y guardarías una lista ligera en memoria de las rutas y anotaciones.
        self.image_paths = [os.path.join(self.root_dir, "images", "0000f77c-6257be58.jpg")] # Mock
        self.annotations = [{"boxes": [[10, 20, 100, 200]], "category": "car"}] # Mock
        print(f"[BDD100K] Indexados {len(self.image_paths)} elementos desde {self.root_dir}")

    def get_image(self, idx: int) -> np.ndarray:
        # Aquí se usaría cv2.imread() o PIL.Image.open()
        # Mock devolviendo una imagen negra
        return np.zeros((720, 1280, 3), dtype=np.uint8)
    
    def get_labels(self, idx: int) -> Tuple[np.ndarray, np.ndarray]:
        # Extraer data de self.annotations[idx] y normalizarla
        boxes = np.array(self.annotations[idx]["boxes"], dtype=np.float32)
        labels = np.array([0]) # 0 = car, en nuestro mapeo universal
        return boxes, labels

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "BDD100K Official",
            "resolution": (1280, 720),
            "classes": ["car", "bus", "person", "bike", "truck", "motor", "train", "rider", "traffic sign", "traffic light"]
        }
    
    def __len__(self) -> int:
        return len(self.image_paths)
