import os
import matplotlib.pyplot as plt
import networkx as nx

# Definição do Grafo (Bairros da Serra - ES)
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
    'A': 'Laranjeiras\n(Origem)',
    'B': 'Valparaíso',
    'C': 'Colina de\nLaranjeiras',
    'D': 'Morada de\nLaranjeiras',
    'E': 'Bicanga',
    'F': 'Manguinhos',
    'G': 'Feu Rosa',
    'H': 'Jacaraípe\n(Destino)'
}

# Posições personalizadas dos nós baseadas no mapa/diagrama do artigo
posicoes = {
    'A': (0.0, 2.0),
    'B': (2.0, 4.0),
    'C': (2.0, 2.0),
    'D': (2.0, 0.0),
    'G': (5.0, 4.0),
    'E': (5.0, 2.0),
    'F': (5.0, 0.0),
    'H': (7.2, 2.0)
}

# Rota ótima calculada pelo Dijkstra: A -> C -> D -> E -> F -> H (22 min)
rota_otima = ['A', 'C', 'D', 'E', 'F', 'H']
arestas_rota_otima = list(zip(rota_otima[:-1], rota_otima[1:]))
arestas_rota_otima_set = set(arestas_rota_otima) | {(v, u) for u, v in arestas_rota_otima}

def construir_grafo_nx():
    G = nx.Graph()
    for u, vizinhos in grafo_serra.items():
        for v, peso in vizinhos.items():
            G.add_edge(u, v, weight=peso)
    return G

def plotar_grafo(destacar_rota=True, salvar_como="grafo_rota_otima.png"):
    G = construir_grafo_nx()
    fig, ax = plt.subplots(figsize=(12, 7.5))

    # Separação das arestas
    arestas_normais = [e for e in G.edges() if e not in arestas_rota_otima_set]
    arestas_destaque = [e for e in G.edges() if e in arestas_rota_otima_set]

    # Desenhar arestas normais
    nx.draw_networkx_edges(
        G, posicoes,
        edgelist=arestas_normais,
        width=2.0,
        edge_color='#888888',
        style='solid',
        alpha=0.6,
        ax=ax
    )

    # Se solicitado, destacar rota ótima (vermelho / espesso como no artigo)
    if destacar_rota:
        nx.draw_networkx_edges(
            G, posicoes,
            edgelist=arestas_destaque,
            width=5.0,
            edge_color='#D9381E',
            alpha=0.85,
            ax=ax
        )
    else:
        nx.draw_networkx_edges(
            G, posicoes,
            edgelist=arestas_destaque,
            width=2.0,
            edge_color='#888888',
            alpha=0.6,
            ax=ax
        )

    # Desenhar os nós
    cores_nos = []
    for node in G.nodes():
        if node == 'A':
            cores_nos.append('#4CAF50')  # Origem (Verde)
        elif node == 'H':
            cores_nos.append('#E53935')  # Destino (Vermelho)
        elif destacar_rota and node in rota_otima:
            cores_nos.append('#FFB74D')  # Bairros intermediários da rota (Laranja suave)
        else:
            cores_nos.append('#ECEFF1')  # Demais nós (Cinza claro)

    nx.draw_networkx_nodes(
        G, posicoes,
        node_color=cores_nos,
        node_size=2000,
        edgecolors='#263238',
        linewidths=2.5,
        ax=ax
    )

    # Rótulo interno (Letra do Vértice)
    nx.draw_networkx_labels(
        G, posicoes,
        labels={node: node for node in G.nodes()},
        font_size=14,
        font_weight='bold',
        font_family='sans-serif',
        ax=ax
    )

    # Rótulos externos com os nomes dos bairros
    deslocamento_y = {
        'A': -0.45,
        'B': 0.45,
        'C': -0.48,
        'D': -0.48,
        'G': 0.45,
        'E': 0.45,
        'F': -0.48,
        'H': -0.45
    }
    
    for node, (x, y) in posicoes.items():
        ax.text(
            x, y + deslocamento_y[node],
            nomes[node],
            fontsize=10.5,
            ha='center',
            va='center',
            fontweight='semibold',
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#B0BEC5", alpha=0.9)
        )

    # Desenhar pesos das arestas (tempo em minutos)
    pesos = nx.get_edge_attributes(G, 'weight')
    rotulos_pesos = {edge: f"{peso} min" for edge, peso in pesos.items()}
    nx.draw_networkx_edge_labels(
        G, posicoes,
        edge_labels=rotulos_pesos,
        font_size=9.5,
        font_color='#1A237E',
        bbox=dict(boxstyle="round,pad=0.2", fc="#FFF9C4", ec="#FBC02D", alpha=0.9),
        ax=ax
    )

    if destacar_rota:
        titulo = (
            "Grafo de Entregas na Serra (ES) - Rota Ótima (Dijkstra)\n"
            "Laranjeiras (A) ➔ Colina (C) ➔ Morada (D) ➔ Bicanga (E) ➔ Manguinhos (F) ➔ Jacaraípe (H)\n"
            "Tempo Total Mínimo: 22 minutos"
        )
    else:
        titulo = "Modelagem da Malha Viária de Entregas - Município da Serra (ES)\n(8 Vértices e 13 Arestas Ponderadas)"

    ax.set_title(titulo, fontsize=13, fontweight='bold', pad=25)
    ax.margins(0.18)
    ax.axis('off')
    plt.tight_layout()

    caminho_completo = os.path.abspath(salvar_como)
    plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Imagem gerada: {caminho_completo}")

if __name__ == "__main__":
    # Gera ambas as visualizações: o grafo original e com a rota destacada
    plotar_grafo(destacar_rota=False, salvar_como="grafo_malha_viaria.png")
    plotar_grafo(destacar_rota=True, salvar_como="grafo_rota_otima.png")

