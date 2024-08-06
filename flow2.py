class Graph:
    def __init__(self, vertices):
        self.graph = {v: {} for v in vertices}
        self.vertices = vertices

    def add_edge(self, u, v, capacity,flow=0):
        self.graph[u][v] = {'capacity': capacity, 'flow': 0}
        if v not in self.graph:
            self.graph[v] = {}

    def _dfs(self, source, sink, visited):
        stack = [(source, float('Inf'))]
        paths = {source: []}
        
        while stack:
            u, flow = stack.pop()
            if u == sink:
                return paths[sink], flow
            visited.add(u)
            for v in self.graph[u]:
                residual_capacity = self.graph[u][v]['capacity'] - self.graph[u][v]['flow']
                if v not in visited and residual_capacity > 0:
                    paths[v] = paths[u] + [(u, v)]
                    stack.append((v, min(flow, residual_capacity)))
                    if v == sink:
                        return paths[sink], min(flow, residual_capacity)
        return None, 0

    def ford_fulkerson(self, source, sink):
        max_flow = 0
        while True:
            visited = set()
            path, flow = self._dfs(source, sink, visited)
            if not path:
                break
            max_flow += flow
            for u, v in path:
                self.graph[u][v]['flow'] += flow
                if v in self.graph and u in self.graph[v]:
                    self.graph[v][u]['flow'] -= flow
                else:
                    self.graph[v][u] = {'capacity': 0, 'flow': -flow}
        return max_flow


# Example Usage
vertices = [
    'E', 'a', 'b', 'c', 
    'd', 'e', 'f', 
    'g','S'
]
g = Graph(vertices)
# Add edges based on the given graph
g.add_edge('E', 'a', 5, 5)
g.add_edge('E', 'c', 8, 8)
g.add_edge('E', 'b', 10, 10)
g.add_edge('a', 'd', 7, 7)
g.add_edge('a', 'e', 10, 10)
g.add_edge('b', 'e', 2, 2)
g.add_edge('b', 'c', 1, 1)
g.add_edge('b', 'd', 8, 8)
g.add_edge('c', 'e', 2, 2)
g.add_edge('c', 'f', 4, 4)
g.add_edge('d', 'g', 7, 7)
g.add_edge('e', 'g', 4, 4)
g.add_edge('e', 'S', 6, 6)
g.add_edge('e', 'f', 2, 2)
g.add_edge('g', 'S', 10, 10)
g.add_edge('f', 'S', 6, 6)
# g.add_edge('T4', 'R', 8000, 6000)
# g.add_edge('T5', 'R', 4000, 2000)

# # Add super source S and connect it to S1, S2, S3
# g.add_edge('S', 'S1', 100000,0)
# g.add_edge('S', 'S2', 100000,0)
# g.add_edge('S', 'S3', 100000,0)

source = 'E'
sink = 'S'
print(f"Max Flow: {g.ford_fulkerson(source, sink)}")
