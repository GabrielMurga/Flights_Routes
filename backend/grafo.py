import math
from models import Rota

def montar_grafo(rotas: list[Rota]) -> dict[int, list[int]]:
    grafo = {}

    for rota in rotas:
        if rota.origem_id not in grafo:
            grafo[rota.origem_id] = []
        grafo[rota.origem_id].append(rota.destino_id)

    return grafo


def haversine(lat1: float, lon1: float, lat2: float, lon2: float):
    raio_terra = 6371.0

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return raio_terra * c