import numpy as np
from typing import Tuple, Dict, Any
import os
import csv

from src.datasets.core.base_dataset import BaseDataset
from src.datasets.core.registry import register_dataset

@register_dataset("cnrpark")
class CNRParkDataset(BaseDataset):
    """
    Implementación para leer CNRPark-EXT.
    Responsabilidad: Parsear los archivos CSV que dictan la ruta de la imagen y su etiqueta.
    """
    def _load_index(self) -> None:
        self.data = []
        # csv_path = os.path.join(self.root_dir, "LABELS", "all.txt")
        # Aquí se abriría el archivo de texto/CSV y se leerían las filas
        print(f"[CNRPark] Indexando metadatos desde CSV en {self.root_dir}...")
        
    def get_image(self, idx: int) -> np.ndarray:
        return np.zeros((720, 1280, 3), dtype=np.uint8)
    
    def get_labels(self, idx: int) -> Tuple[np.ndarray, np.ndarray]:
        # Se convierte la fila del CSV a bounding boxes o etiquetas simples
        boxes = np.empty((0, 4), dtype=np.float32)
        labels = np.array([])
        return boxes, labels

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "CNRPark-EXT",
            "classes": ["free", "busy"]
        }
    
    def __len__(self) -> int:
        return len(self.data)
