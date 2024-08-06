def add_edge(graph, from_node, to_node, weight):
    if from_node not in graph:
        graph[from_node] = {}
    graph[from_node][to_node] = weight

def initialize_graph(edges):
    graph = {}
    for edge in edges:
        from_node, to_node, weight,undirected = edge
        add_edge(graph, from_node, to_node, weight)
        if undirected:
            add_edge(graph, to_node, from_node, weight)  # Assuming undirected graph
    return graph