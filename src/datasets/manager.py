import os
from typing import List, Dict, Type
from torch.utils.data import Dataset, ConcatDataset

from src.datasets.core.registry import get_dataset_class
from src.datasets.core.base_dataset import BaseDataset

class DataManager:
    """
    Facade que orquesta la carga de los datasets.
    Oculta al usuario la complejidad de buscar rutas, instanciar clases y combinar datasets.
    """
    
    def __init__(self, config: Dict[str, str]):
        self.config = config

    def load_dataset(self, name: str, split: str = 'train') -> BaseDataset:
        """
        Instancia un dataset registrado buscándolo en el Registry.
        """
        # 1. Recuperar la clase desde el Registry (OCP)
        dataset_class: Type[BaseDataset] = get_dataset_class(name.lower())
        
        # 2. Buscar la ruta configurada
        env_key = f"{name.upper()}_PATH"
        dataset_path = self.config.get(env_key)
        
        if not dataset_path or not os.path.exists(dataset_path):
            # Fallback opcional o lanzamiento de error estricto
            raise FileNotFoundError(
                f"No se encontró la ruta física para el dataset '{name}'. "
                f"Asegúrate de definir {env_key} en tu .env y de que la carpeta exista en {dataset_path}."
            )
            
        # 3. Retornar la instancia del dataset
        return dataset_class(root_dir=dataset_path, split=split)

    def combine(self, dataset_names: List[str], split: str = 'train') -> Dataset:
        """
        Combina múltiples datasets en uno solo continuo, ideal para entrenamiento conjunto.
        """
        datasets = []
        for name in dataset_names:
            ds = self.load_dataset(name, split)
            datasets.append(ds)
            
        if not datasets:
            raise ValueError("No se pasaron datasets para combinar.")
            
        # PyTorch ConcatDataset abstrae la lectura contigua de varios Datasets
        return ConcatDataset(datasets)
