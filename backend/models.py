from dataclasses import dataclass
from typing import Optional

@dataclass
class Aeroporto:
    id: int
    nome: str
    cidade: str
    pais: str
    iata: Optional[str]
    latitude: float
    longitude: float

@dataclass
class Rota:
    origem_id: int
    destino_id: int