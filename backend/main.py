from parser import ler_aeroportos, ler_rotas
from grafo import montar_grafo
from dijkstra import dijkstra

def main():
    aeroportos = ler_aeroportos("../airports.dat")
    rotas = ler_rotas("../routes.dat")
    grafo = montar_grafo(rotas)

    resultado = dijkstra(grafo, aeroportos, 2564, 2279)

    if resultado is None:
        print("Sem rota encontrada")
        return

    distancia, caminho = resultado

    print(f"Distância total: {distancia:.0f} km")
    print("Caminho: ", end="")
    for i, id in enumerate(caminho):
        a = aeroportos[id]
        if i == len(caminho) - 1:
            print(a.iata)
        else:
            print(f"{a.iata} → ", end="")

if __name__ == "__main__":
    main()