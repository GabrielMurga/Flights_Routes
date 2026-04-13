from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from parser import ler_aeroportos, ler_rotas
from grafo import montar_grafo
from dijkstra import dijkstra

app = FastAPI()

# permite o front chamar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

aeroportos = ler_aeroportos("../airports.dat")
rotas = ler_rotas("../routes.dat")
grafo = montar_grafo(rotas)

#IATA pra ID 
iata_para_id = {}
for id, a in aeroportos.items():
    if a.iata:
        iata_para_id[a.iata] = id


@app.get("/rota")
def buscar_rota(origem: str, destino: str,modo: str = "distancia"):
    origem_id = iata_para_id.get(origem.upper())
    destino_id = iata_para_id.get(destino.upper())

    if not origem_id:
        raise HTTPException(status_code=404, detail=f"Aeroporto {origem} não encontrado")
    if not destino_id:
        raise HTTPException(status_code=404, detail=f"Aeroporto {destino} não encontrado")

    resultado = dijkstra(grafo, aeroportos, origem_id, destino_id,modo)

    if resultado is None:
        raise HTTPException(status_code=404, detail="Sem rota encontrada entre esses aeroportos")

    distancia, caminho = resultado

    if modo == "escalas":
            return {
                "escalas": round(distancia),
                "caminho": [
                    {
                        "iata": aeroportos[id].iata,
                        "nome": aeroportos[id].nome,
                        "lat": aeroportos[id].latitude,
                        "lon": aeroportos[id].longitude,
                    }
                    for id in caminho
                ]
            }
    else:
            return {
                "distancia_km": round(distancia),
                "caminho": [
                    {
                        "iata": aeroportos[id].iata,
                        "nome": aeroportos[id].nome,
                        "lat": aeroportos[id].latitude,
                        "lon": aeroportos[id].longitude,
                    }
                    for id in caminho
                ]
            }



@app.get("/rotas/{iata}")
def rotas_do_aeroporto(iata: str):
    origem_id = iata_para_id.get(iata.upper())

    if not origem_id:
        raise HTTPException(status_code=404, detail=f"Aeroporto {iata} não encontrado")

    destinos = grafo.get(origem_id, [])

    return {
        "aeroporto": iata.upper(),
        "lat": aeroportos[origem_id].latitude,
        "lon": aeroportos[origem_id].longitude,
        "total": len(destinos),
        "destinos": [
            {
                "iata": aeroportos[id].iata,
                "nome": aeroportos[id].nome,
                "lat": aeroportos[id].latitude,
                "lon": aeroportos[id].longitude,
            }
            for id in destinos
            if id in aeroportos and aeroportos[id].iata
        ]
    }



@app.get("/aeroportos")
def buscar_aeroportos(busca: str):
    busca = busca.lower()
    resultados = []

    for id, a in aeroportos.items():
        if (busca in a.nome.lower() or
            busca in a.cidade.lower() or
            busca in a.pais.lower() or
            (a.iata and busca in a.iata.lower())):
            resultados.append({
                "iata": a.iata,
                "nome": a.nome,
                "cidade": a.cidade,
                "pais": a.pais,
                "rotas": len(grafo.get(id, []))
            })

    resultados.sort(key=lambda x: x["rotas"], reverse=True)

    return {"total": len(resultados), "resultados": resultados[:50]}