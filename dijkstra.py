import heapq
import networkx as nx
import matplotlib.pyplot as plt

from sys import argv

from utils import initialize_graph

def dijkstra(graph, start):
    # Number of nodes in the graph
    n = len(graph)
    
    # Distances array, initially set to infinity
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0  # Distance to the source is 0
    
    # Previous nodes to reconstruct the path
    previous_nodes = {node: None for node in graph}
    
    # Priority queue to process nodes in order of their distance from the source
    priority_queue = [(0, start)]  # (distance, node)
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Nodes can get added to the priority queue multiple times, we only process each node once
        if current_distance > distances[current_node]:
            continue
        
        # Update the distance to each neighbor
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            # Only consider this new path if it's better
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    print(priority_queue)
    
    return distances, previous_nodes
 

def reconstruct_path(previous_nodes, start, end):
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.reverse()
    if path[0] == start:
        return path
    else:
        return []

def plot_graph(graph, start_node, distances, previous_nodes):
    G = nx.DiGraph()

    for node, edges in graph.items():
        for neighbor, weight in edges.items():
            G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    
    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    plt.title(f'Shortest Paths from Node {start_node}')
    plt.show()

edges=[
    ('a','b',4,False),
    ('a','c',6,False),
    ('b','e',2,False),
    ('b','d',6,False),
    ('c','e',2,False),
    ('c','f',3,False),
    ('d','g',2,False),
    ('e','d',4,False),
    ('e','h',6,False),
    ('e','i',1,False),
    ('f','i',8,False),
    ('g','j',7,False),
    ('h','j',2,False),
    ('i','j',3,False),
    ('j','j',0,False),
    
]

graph = initialize_graph(edges)


print(graph)
# Find the shortest paths from node 1
start_node = argv[1]
distances, previous_nodes = dijkstra(graph, start_node)
print(previous_nodes)
print("Shortest paths from node 1:")
for node, distance in distances.items():
    print(f"Node {node}: Distance = {distance}, Path = {reconstruct_path(previous_nodes, start_node, node)}")

plot_graph(graph, start_node, distances, previous_nodes)

