import heapq
import networkx as nx
import matplotlib.pyplot as plt

from utils import initialize_graph
from sys import argv


def bellman_ford(graph, start, destination):
    # Step 1: Initialize distances from start to all other nodes as infinity
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0

    # Step 2: Initialize the previous nodes dictionary
    previous_nodes = {node: None for node in graph}

    # Step 3: Relax all edges |V| - 1 times
    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph[node].items():
                if  distances[node]!=float('infinity') and distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
                    previous_nodes[neighbor] = node

    # Step 4: Check for negative-weight cycles
    for node in graph:
        for neighbor, weight in graph[node].items():
            if distances[node] + weight < distances[neighbor]:
                print("Graph contains a negative-weight cycle")
                return distances[destination], None

    # Step 5: Reconstruct the path from start to destination
    path = []
    current_node = destination
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.reverse()

    if path[0] == start:
        return distances[destination], path
    else:
        return float('infinity'), []
    
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
start_node = argv[1]
end_node = argv[2]
distance, path = bellman_ford(graph, start_node, end_node)
if path:
    print(f"Shortest path from node '{start_node}' to node '{end_node}': {path} with distance {distance}")
else:
    print(distance)
    print("No path found or graph contains a negative-weight cycle")