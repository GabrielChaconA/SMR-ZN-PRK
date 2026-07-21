from torch.utils.data import Dataset
from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, Any, Tuple

class BaseDataset(Dataset, ABC):
    """
    Contrato base estricto para todos los datasets.
    Garantiza que cualquier clase de dataset (BDD100K, Cityscapes) exponga los mismos métodos.
    """
    
    def __init__(self, root_dir: str, split: str = 'train', transform=None):
        """
        Args:
            root_dir (str): Ruta base al dataset en el disco local.
            split (str): Subconjunto ('train', 'val', 'test').
            transform: Transformaciones de Data Augmentation a aplicar (ej. albumentations).
        """
        self.root_dir = root_dir
        self.split = split
        self.transform = transform
        self._load_index()
        
    @abstractmethod
    def _load_index(self):
        """Método interno para escanear y cargar la lista de imágenes/anotaciones del dataset sin cargarlas en RAM."""
        pass

    @abstractmethod
    def load_image(self, idx: int) -> np.ndarray:
        """Carga una imagen específica desde el disco a un array RGB de numpy."""
        pass
    
    @abstractmethod
    def load_annotation(self, idx: int) -> Dict[str, Any]:
        """Carga y parsea la anotación original del dataset (JSON, XML, TXT)."""
        pass
    
    @abstractmethod
    def unify_format(self, image: np.ndarray, annotation: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Convierte la etiqueta propietaria a un formato universal para la red (ej. COCO/YOLO format).
        Aquí también se aplica Data Augmentation si self.transform no es None.
        """
        pass

    def __getitem__(self, idx: int) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Método requerido por PyTorch DataLoader."""
        image = self.load_image(idx)
        annotation = self.load_annotation(idx)
        image_unified, annot_unified = self.unify_format(image, annotation)
        return image_unified, annot_unified
