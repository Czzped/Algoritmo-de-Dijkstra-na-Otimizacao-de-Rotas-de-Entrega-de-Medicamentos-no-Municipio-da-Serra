import heapq

def dijkstra(grafo, inicio, destino):
    distancias = {vertice: float('inf') for vertice in grafo}
    distancias[inicio] = 0
    anteriores = {vertice: None for vertice in grafo}
    fila = [(0, inicio)]

    while fila:
        dist_atual, atual = heapq.heappop(fila)

        if atual == destino:
            break
        if dist_atual > distancias[atual]:
            continue

        for vizinho, peso in grafo[atual].items():
            nova_dist = dist_atual + peso
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                anteriores[vizinho] = atual
                heapq.heappush(fila, (nova_dist, vizinho))

    # Reconstrução do caminho mínimo
    caminho = []
    atual = destino
    while atual is not None:
        caminho.insert(0, atual)
        atual = anteriores[atual]

    return caminho, distancias[destino]

# Grafo dos bairros da Serra (pesos em minutos)
grafo_serra = {
    'A': {'B': 3, 'C': 5, 'D': 12},
    'B': {'A': 3, 'C': 3, 'G': 9},
    'C': {'A': 5, 'B': 3, 'D': 4, 'G': 8},
    'D': {'A': 12, 'C': 4, 'E': 5, 'F': 8},
    'E': {'D': 5, 'F': 2, 'G': 6, 'H': 11},
    'F': {'D': 8, 'E': 2, 'H': 6},
    'G': {'B': 9, 'C': 8, 'E': 6},
    'H': {'E': 11, 'F': 6}
}

nomes = {
    'A': 'Laranjeiras',
    'B': 'Valparaíso',
    'C': 'Colina de Laranjeiras',
    'D': 'Morada de Laranjeiras',
    'E': 'Bicanga',
    'F': 'Manguinhos',
    'G': 'Feu Rosa',
    'H': 'Jacaraípe'
}

caminho, tempo_total = dijkstra(grafo_serra, 'A', 'H')
rota_nomes = " -> ".join(f"{nomes[v]} ({v})" for v in caminho)

print(f"Melhor rota: {rota_nomes}")
print(f"Tempo total estimado: {tempo_total} minutos")
