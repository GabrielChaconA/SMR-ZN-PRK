from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import numpy as np

@dataclass
class DetectionSample:
    """
    Estructura de datos universal que el pipeline de ML espera recibir.
    Elimina la dependencia de diccionarios crudos y estandariza los formatos
    independientemente del origen de los datos (JSON, CSV, Directorios).
    """
    image: np.ndarray
    boxes: np.ndarray  # Formato estándar esperado: [N, 4] -> [x_min, y_min, x_max, y_max]
    labels: np.ndarray # Formato estándar esperado: [N] -> IDs enteros de clase
    metadata: Dict[str, Any] = field(default_factory=dict)
