import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import heapq

place = "Manhattan, New York, USA"
G = ox.graph_from_place(place, network_type="drive", simplify=True)
G = ox.distance.add_edge_lengths(G)

print("init graph")

nodes = list(G.nodes())
start, end = nodes[10], nodes[30]  # Можно изменить индексы

# Реализация Дейкстры с записью посещённых вершин
def dijkstra_visited_nodes(G, start, end):
    print("start dijkstra")
    distances = {node: float('inf') for node in G.nodes()}
    distances[start] = 0
    heap = [(0, start)]
    visited = set()
    visited_nodes_order = []  # Для хранения порядка посещения
    
    while heap:
        current_dist, current_node = heapq.heappop(heap)
        if current_node in visited:
            continue
        visited.add(current_node)
        visited_nodes_order.append(current_node)
        
        if current_node == end:
            break
            
        for neighbor in G.neighbors(current_node):
            edge_data = G.get_edge_data(current_node, neighbor)
            new_dist = current_dist + edge_data[0]['length']
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    
    print("finish dijkstra")
    return visited_nodes_order

# Получаем список посещённых вершин
visited_nodes = dijkstra_visited_nodes(G, start, end)

print("draw")
# Визуализация
fig, ax = ox.plot_graph(
    G,
    show=False,
    close=False,
    node_size=0,  # Исходные вершины не отображаем
    edge_linewidth=0.5,
    edge_color="gray"
)

# Подсвечиваем посещённые вершины
ox.plot_graph(
    G.subgraph(visited_nodes),  # Только посещённые вершины
    ax=ax,
    node_color="red",  # Красный = посещённые
    node_size=20,
    edge_color="blue",  # Рёбра между посещёнными вершинами
    edge_linewidth=1
)

# Отмечаем стартовую и конечную вершины
ox.plot_graph(
    G.subgraph([start, end]),
    ax=ax,
    node_color="green",  # Зелёный = start/end
    node_size=50
)

plt.title(f"Вершины, просмотренные Дейкстрой (n={len(visited_nodes)})")
plt.show()