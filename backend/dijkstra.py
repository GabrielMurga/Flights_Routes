import math
from models import Aeroporto
from grafo import haversine

def dijkstra(
    grafo: dict[int, list[int]],
    aeroportos: dict[int, Aeroporto],
    origem: int,
    destino: int,
    modo: str = "distancia"
) -> tuple[float, list[int]] | None:

    distancias = {origem: 0.0}
    anteriores = {}
    visitados = set()
    nao_visitados = {origem}

    while nao_visitados:
        atual = None
        menor_dist = float('inf')

        for no in nao_visitados:
            if no in distancias:
                dist = distancias[no]
            else:
                dist = float('inf')

            if dist < menor_dist:
                menor_dist = dist
                atual = no

        if atual is None or atual == destino:
            break

        nao_visitados.remove(atual)
        visitados.add(atual)

        for vizinho in grafo.get(atual, []):
            if vizinho in visitados:
                continue

            a1 = aeroportos.get(atual)
            a2 = aeroportos.get(vizinho)

            if not a1 or not a2:
                continue

            
            if modo == "escalas":
                peso = 1
            else:
                peso = haversine(a1.latitude, a1.longitude, a2.latitude, a2.longitude)
            nova_dist = distancias[atual] + peso

            if vizinho in distancias:
                dist_vizinho = distancias[vizinho]
            else:
                dist_vizinho = float('inf')

            if nova_dist < dist_vizinho:
                distancias[vizinho] = nova_dist # atualizo
                anteriores[vizinho] = atual
                nao_visitados.add(vizinho)

    if destino not in distancias:
        return None

    caminho = []
    atual = destino
    while atual != origem:
        caminho.append(atual)
        atual = anteriores[atual]
    caminho.append(origem)
    caminho.reverse()

    return distancias[destino], caminho