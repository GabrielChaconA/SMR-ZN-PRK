from torch.utils.data import Dataset
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
import numpy as np

from src.datasets.core.types import DetectionSample

class BaseDataset(Dataset, ABC):
    """
    Contrato estricto que todos los datasets deben implementar (Liskov Substitution Principle).
    Garantiza que sin importar si la fuente es JSON, CSV o Carpetas, la salida siempre
    será un objeto DetectionSample tipado.
    """
    
    def __init__(self, root_dir: str, split: str = 'train', transform=None):
        self.root_dir = root_dir
        self.split = split
        self.transform = transform
        
        # Carga perezosa (lazy loading) del índice en memoria
        self._load_index()
        
    @abstractmethod
    def _load_index(self) -> None:
        """
        Debe escanear el dataset (JSON, CSV, Directorio) y poblar una lista interna 
        (ej. self.image_paths, self.annotations) sin cargar los datos masivos a la RAM.
        """
        pass

    @abstractmethod
    def get_image(self, idx: int) -> np.ndarray:
        """Debe cargar la imagen física del disco y devolverla como array Numpy (RGB)."""
        pass
    
    @abstractmethod
    def get_labels(self, idx: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Debe procesar la metadata específica del dataset y devolver las cajas y etiquetas
        normalizadas.
        Returns:
            boxes: array de forma [N, 4] con coordenadas [x_min, y_min, x_max, y_max]
            labels: array de forma [N] con IDs de clases
        """
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Devuelve información global del dataset (ej. clases disponibles, versión)."""
        pass

    def __getitem__(self, idx: int) -> DetectionSample:
        """
        Implementación obligatoria de PyTorch Dataset.
        Actúa como un Template Method: orquesta la carga, aplica transformaciones
        y construye la respuesta final.
        """
        image = self.get_image(idx)
        boxes, labels = self.get_labels(idx)
        
        # Opcional: Aquí se aplicarían transformaciones visuales (Data Augmentation)
        # si self.transform no es None.
        if self.transform:
            # Ejemplo con albumentations:
            # transformed = self.transform(image=image, bboxes=boxes, class_labels=labels)
            # image = transformed['image']
            # boxes = np.array(transformed['bboxes'])
            # labels = np.array(transformed['class_labels'])
            pass
            
        return DetectionSample(
            image=image,
            boxes=boxes,
            labels=labels,
            metadata={"dataset_idx": idx, "split": self.split}
        )
