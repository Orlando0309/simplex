def calculate_degrees(graph):
    degrees = {vertex: len(neighbors) for vertex, neighbors in graph.items()}
    return degrees

def sort_vertices_by_degree(graph):
    degrees = calculate_degrees(graph)
    sorted_vertices = sorted(degrees, key=degrees.get, reverse=True)
    return sorted_vertices

def graph_coloring(graph):
    sorted_vertices = sort_vertices_by_degree(graph)
    color_map = {}
    color = 0
    
    for vertex in sorted_vertices:
        if vertex not in color_map:
            color_map[vertex] = color
            for neighbor in sorted_vertices:
                if neighbor not in color_map and not any(neighbor in graph[v] for v in color_map if color_map[v] == color):
                    color_map[neighbor] = color
            color += 1
            
    return color_map

# Exemple de graphe représenté par un dictionnaire d'adjacence
graph = {
    'A': ['B', 'C','D','G','H'],
    'B': ['E', 'C','D','G'],
    'C': [ 'F','D','G'],
    'D': ['F'],
    'E':['F','G'],
    'F':['G']
}

# Appel de la fonction de coloration de graphe
coloration = graph_coloring(graph)
print(coloration)
