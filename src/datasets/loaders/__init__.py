# Al importar este paquete, se importan automáticamente las clases concretas
# Esto provoca que el decorador @register_dataset se ejecute y registre los datasets en el DataManager.

from .bdd100k_dataset import BDD100KDataset
from .pklot_dataset import PKLotDataset
from .cnrpark_dataset import CNRParkDataset

__all__ = ["BDD100KDataset", "PKLotDataset", "CNRParkDataset"]
