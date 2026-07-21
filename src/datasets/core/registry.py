from typing import Callable, Dict, Type

_DATASET_REGISTRY: Dict[str, Type] = {}

def register_dataset(name: str) -> Callable:
    """
    Decorador para registrar automáticamente una clase de Dataset en el sistema.
    Esto cumple con el principio Open/Closed: Puedes agregar nuevos datasets
    sin modificar el DataManager.
    
    Uso:
        @register_dataset("bdd100k")
        class BDD100KDataset(BaseDataset):
            ...
    """
    def register_dataset_cls(cls: Type) -> Type:
        if name in _DATASET_REGISTRY:
            raise ValueError(f"El dataset '{name}' ya está registrado.")
        _DATASET_REGISTRY[name] = cls
        return cls
    return register_dataset_cls

def get_dataset_class(name: str) -> Type:
    """Recupera la clase de dataset registrada por su nombre."""
    if name not in _DATASET_REGISTRY:
        raise KeyError(
            f"Dataset '{name}' no encontrado. "
            f"Datasets disponibles: {list(_DATASET_REGISTRY.keys())}"
        )
    return _DATASET_REGISTRY[name]
