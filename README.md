# Flight Router

Visualizador interativo de rotas aéreas mundiais. Encontra o menor caminho entre dois aeroportos usando o algoritmo de Dijkstra, com mapa animado mostrando o avião percorrendo a rota.

---

## Sobre o projeto

Um projeto pessoal com foco em algoritmos de grafos, arquitetura de APIs e visualização de dados geográficos.

A malha aérea mundial é modelada como um grafo dirigido — aeroportos são nós e rotas comerciais são arestas com peso baseado na distância geográfica real (fórmula de Haversine). O algoritmo de Dijkstra encontra o caminho ótimo entre qualquer par de aeroportos do mundo.

A analogia direta é um "Google Maps de aviões" — o mesmo problema de caminho mínimo, aplicado à aviação.

---

## Stack

- **Backend** — Python, FastAPI
- **Algoritmo** — Dijkstra implementado do zero
- **Frontend** — HTML, CSS, JavaScript, Leaflet.js
- **Dados** — OpenFlights (7.698 aeroportos, 67.240 rotas reais)

---

## Funcionalidades

- Rota com menor distância em km entre dois aeroportos
- Rota com menor número de escalas
- Visualização de todas as rotas diretas de um aeroporto
- Busca de aeroportos por cidade, nome ou código IATA
- Mapa interativo com avião animado percorrendo a rota

---

## Arquitetura

frontend/
├── index.html       # mapa interativo
├── aeroportos.html  # busca de aeroportos
├── script.js        # lógica do mapa e chamadas à API
└── style.css        # estilos
backend/
├── api.py           # endpoints FastAPI
├── dijkstra.py      # algoritmo de Dijkstra
├── grafo.py         # lista de adjacência e Haversine
├── parser.py        # leitura dos arquivos .dat
└── models.py        # structs Aeroporto e Rota

---

## O algoritmo

O grafo é carregado em memória quando o servidor sobe — 7.698 nós e 67.240 arestas. O Dijkstra roda sob demanda para cada requisição.

Dois modos de busca, mesmo algoritmo, pesos diferentes:

- **Menor distância** — peso da aresta = distância Haversine entre as coordenadas dos aeroportos
- **Menor escalas** — peso da aresta = 1 para todas as conexões

A fórmula de Haversine calcula a distância real entre dois pontos na superfície da Terra usando latitude e longitude, considerando a curvatura do globo.

---

## Dados

Os dados são da base pública [OpenFlights](https://openflights.org/data.html), não incluídos no repositório por tamanho. O script de download está na seção "Como rodar localmente".

---

## Como rodar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/flight-router.git
cd flight-router
```

**2. Baixe os dados**
```bash
curl -O https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat
curl -O https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat
```

**3. Instale as dependências**
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**4. Suba o backend**
```bash
cd backend
uvicorn api:app --reload
```

**5. Abra o frontend**
```bash
cd frontend
python -m http.server 3000
```

Acesse `http://localhost:3000`.

## Autor

Gabriel Losekann Paiva Murga