const map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap © CARTO'
}).addTo(map);

let rotaLayer = null;
let aviaoMarker = null;
let animacaoAtiva = false;

async function buscarRota() {
    const origem = document.getElementById('origem').value.trim();
    const destino = document.getElementById('destino').value.trim();
    const btn = document.getElementById('btn');
    const modo = document.getElementById('modo').value;


    if (!origem || !destino) return;

    btn.disabled = true;
    btn.textContent = 'Buscando...';
    document.getElementById('info').textContent = 'Calculando rota...';

    try {
        const res = await fetch(`http://localhost:8000/rota?origem=${origem}&destino=${destino}&modo=${modo}`);
        const data = await res.json();

        if (!res.ok) {
            document.getElementById('info').textContent = data.detail || 'Erro ao buscar rota.';
            return;
        }

        desenharRota(data);

    } catch (e) {
        document.getElementById('info').textContent = 'Erro ao conectar com a API.';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Buscar';
    }
}

function desenharRota(data) {
    if (rotaLayer) map.removeLayer(rotaLayer);
    if (aviaoMarker) map.removeLayer(aviaoMarker);
    animacaoAtiva = false;

    const pontos = data.caminho.map(a => [a.lat, a.lon]);
    const iatas = data.caminho.map(a => a.iata);

    rotaLayer = L.layerGroup().addTo(map);

    L.polyline(pontos, {
        color: '#2563eb',
        weight: 2,
        opacity: 0.8,
        dashArray: '6 6'
    }).addTo(rotaLayer);

    data.caminho.forEach(a => {
        L.circleMarker([a.lat, a.lon], {
            radius: 5,
            color: '#2563eb',
            fillColor: '#fff',
            fillOpacity: 1,
            weight: 2
        })
        .bindTooltip(a.iata, {
            permanent: true,
            className: 'iata-label',
            offset: [0, -10]
        })
        .addTo(rotaLayer);
    });

    map.fitBounds(L.latLngBounds(pontos), { padding: [40, 40] });

    const escalas = data.caminho.length - 2;
        if (data.distancia_km !== undefined) {
            document.getElementById('info').textContent =
                `${iatas.join(' → ')} · ${data.distancia_km.toLocaleString()} km · ${escalas} escala(s)`;
        } else {
            document.getElementById('info').textContent =
                `${iatas.join(' → ')} · ${data.escalas} escala(s)`;
        }

    animarAviao(pontos);
}

function animarAviao(pontos) {
    if (aviaoMarker) map.removeLayer(aviaoMarker);
    animacaoAtiva = true;

    const aviaoIcon = L.divIcon({
        html: '✈',
        className: '',
        iconSize: [20, 20],
        iconAnchor: [10, 10]
    });

    aviaoMarker = L.marker(pontos[0], { icon: aviaoIcon }).addTo(map);

    let segmento = 0;
    let progresso = 0;
    const velocidade = 0.005;

    function animar() {
        if (!animacaoAtiva || segmento >= pontos.length - 1) return;

        const inicio = pontos[segmento];
        const fim = pontos[segmento + 1];

        progresso += velocidade;

        if (progresso >= 1) {
            progresso = 0;
            segmento++;
            if (segmento >= pontos.length - 1) return;
        }

        const lat = inicio[0] + (fim[0] - inicio[0]) * progresso;
        const lon = inicio[1] + (fim[1] - inicio[1]) * progresso;

        aviaoMarker.setLatLng([lat, lon]);
        requestAnimationFrame(animar);
    }

    animar();
}



async function verRotas() {
    const origem = document.getElementById('origem').value.trim();
    if (!origem) return;

    if (rotaLayer) map.removeLayer(rotaLayer);
    if (aviaoMarker) map.removeLayer(aviaoMarker);

    document.getElementById('info').textContent = 'Carregando rotas...';

    try {
        const res = await fetch(`http://localhost:8000/rotas/${origem}`);
        const data = await res.json();

        if (!res.ok) {
            document.getElementById('info').textContent = data.detail || 'Erro ao buscar rotas.';
            return;
        }

        rotaLayer = L.layerGroup().addTo(map);

        const origemLatLon = [data.lat, data.lon];

        // marcador da origem
        L.circleMarker(origemLatLon, {
            radius: 6,
            color: '#2563eb',
            fillColor: '#fff',
            fillOpacity: 1,
            weight: 2
        })
        .bindTooltip(data.aeroporto, { permanent: true, className: 'iata-label' })
        .addTo(rotaLayer);

        // destinos e linhas
        data.destinos.forEach(a => {
            L.circleMarker([a.lat, a.lon], {
                radius: 3,
                color: '#2563eb',
                fillColor: '#2563eb',
                fillOpacity: 0.6,
                weight: 1
            })
            .bindTooltip(a.iata, { className: 'iata-label' })
            .addTo(rotaLayer);

            L.polyline([origemLatLon, [a.lat, a.lon]], {
                color: '#2563eb',
                weight: 1,
                opacity: 0.3
            }).addTo(rotaLayer);
        });

        map.setView(origemLatLon, 3);

        document.getElementById('info').textContent =
            `${data.aeroporto} → ${data.total} destinos diretos`;

    } catch (e) {
        document.getElementById('info').textContent = 'Erro ao conectar com a API.';
    }
}