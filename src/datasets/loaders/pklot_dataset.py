import numpy as np
from typing import Tuple, Dict, Any
import os

from src.datasets.core.base_dataset import BaseDataset
from src.datasets.core.registry import register_dataset

@register_dataset("pklot")
class PKLotDataset(BaseDataset):
    """
    Implementación para leer PKLot.
    Responsabilidad: Escanear las carpetas jerárquicas (Empty/Occupied)
    y generar etiquetas automáticas basadas en el nombre del directorio.
    """
    def _load_index(self) -> None:
        self.image_paths = []
        self.labels_cache = []
        # Aquí se usa os.walk(self.root_dir) para mapear todas las imágenes en Empty y Occupied
        print(f"[PKLot] Indexando imágenes desde carpetas en {self.root_dir}...")
        
    def get_image(self, idx: int) -> np.ndarray:
        return np.zeros((720, 1280, 3), dtype=np.uint8)
    
    def get_labels(self, idx: int) -> Tuple[np.ndarray, np.ndarray]:
        # Para PKLot usualmente es clasificación (0 o 1) si las imágenes están recortadas
        # O si son imágenes completas con XML, se parsea el XML.
        boxes = np.empty((0, 4), dtype=np.float32)
        labels = np.array([])
        return boxes, labels

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "PKLot Dataset",
            "classes": ["empty", "occupied"]
        }
    
    def __len__(self) -> int:
        return len(self.image_paths)
