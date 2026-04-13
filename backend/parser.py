import csv
from models import Aeroporto, Rota

def ler_aeroportos(caminho: str) -> dict[int, Aeroporto]:
    aeroportos = {}

    with open(caminho, encoding='utf-8') as f:
        leitor = csv.reader(f)
        for linha in leitor:
            try:
                id = int(linha[0])
                iata = linha[4] if linha[4] != '\\N' else None
                latitude = float(linha[6])
                longitude = float(linha[7])

                aeroportos[id] = Aeroporto(
                    id=id,
                    nome=linha[1],
                    cidade=linha[2],
                    pais=linha[3],
                    iata=iata,
                    latitude=latitude,
                    longitude=longitude
                )
            except (ValueError, IndexError):
                continue

    print(f"Aeroportos carregados: {len(aeroportos)}")
    return aeroportos


def ler_rotas(caminho: str) -> list[Rota]:
    rotas = []

    with open(caminho, encoding='utf-8') as f:
        leitor = csv.reader(f)
        for linha in leitor:
            try:
                if linha[3] == '\\N' or linha[5] == '\\N':
                    continue

                origem_id = int(linha[3])
                destino_id = int(linha[5])
                rotas.append(Rota(origem_id=origem_id, destino_id=destino_id))
            except (ValueError, IndexError):
                continue

    print(f"Rotas carregadas: {len(rotas)}")
    return rotas