import os
from typing import Optional, Dict
from torch.utils.data import DataLoader, Dataset
# from src.data.datasets.bdd100k import BDD100KDataset
# from src.data.datasets.cityscapes import CityscapesDataset
# etc...

class DataManager:
    """
    Orquestador principal de datos (Facade/Factory pattern).
    Detecta, inicializa y provee DataLoaders listos para entrenar.
    """
    
    def __init__(self, config: Dict[str, str]):
        """
        Inicializa el DataManager usando un diccionario de configuración
        que contiene las rutas extraídas de .env o config.yaml.
        """
        self.config = config
        self._registry = self._register_datasets()

    def _register_datasets(self) -> Dict[str, type]:
        """Registra (Factory) qué clase corresponde a qué nombre de dataset."""
        # Se comentan las importaciones hasta que las clases estén completamente implementadas
        return {
            # "bdd100k": BDD100KDataset,
            # "cityscapes": CityscapesDataset,
            # "mapillary": MapillaryDataset,
            # "pklot": PKLotDataset,
            # "cnrpark": CNRParkDataset,
            # "custom": CustomDataset
        }

    def get_dataloader(
        self, 
        dataset_name: str, 
        split: str = 'train', 
        batch_size: int = 32, 
        num_workers: int = 4, 
        shuffle: bool = True
    ) -> DataLoader:
        """
        Construye e inicializa el Dataset solicitado y lo envuelve en un DataLoader nativo de PyTorch.
        """
        dataset_class = self._registry.get(dataset_name.lower())
        if not dataset_class:
            raise ValueError(f"Dataset '{dataset_name}' no soportado o no registrado.")
            
        # Determinar la ruta base buscando la variable en la configuración
        # Por ejemplo, para "bdd100k" buscará "BDD100K_PATH"
        env_key = f"{dataset_name.upper()}_PATH"
        dataset_path = self.config.get(env_key)
        
        if not dataset_path or not os.path.exists(dataset_path):
            raise FileNotFoundError(
                f"La ruta para el dataset '{dataset_name}' no se encontró en {dataset_path}. "
                f"Verifica tu archivo .env o config.yaml."
            )

        # Instanciar usando el contrato BaseDataset
        dataset_instance: Dataset = dataset_class(
            root_dir=dataset_path, 
            split=split,
            transform=self._get_default_transforms()
        )
        
        # Devolver DataLoader para PyTorch
        return DataLoader(
            dataset_instance,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=num_workers,
            pin_memory=True # Optimización para GPUs
        )

    def _get_default_transforms(self):
        """Retorna las transformaciones/DataAugmentation base del pipeline."""
        # Aquí iría lógica de albumentations/torchvision
        return None
