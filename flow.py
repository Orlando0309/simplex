from collections import defaultdict, deque

class Graph:
    def __init__(self):
        self.capacity = defaultdict(dict)
        self.flow = defaultdict(lambda: defaultdict(int))
        self.paths = []  # To store paths used to achieve max flow

    def add_edge(self, u, v, w, f=0):
        self.capacity[u][v] = w
        self.flow[u][v] = 0
        if v not in self.capacity:
            self.capacity[v] = {}

    def bfs(self, source, sink, parent):
        visited = set()
        queue = deque([source])
        visited.add(source)

        while queue:
            u = queue.popleft()
            for v in self.capacity[u]:
                if v not in visited and self.capacity[u][v] - self.flow[u][v] > 0:
                    queue.append(v)
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
        return False
    
    def ford_fulkerson(self, source, sink):
        parent = {}
        max_flow = 0
        
        while self.bfs(source, sink, parent):
            path_flow = float('Inf')
            s = sink
            path = []  # Store current path
            while s != source:
                path_flow = min(path_flow, self.capacity[parent[s]][s] - self.flow[parent[s]][s])
                path.append((parent[s], s))
                s = parent[s]
            path.reverse()
            self.paths.append((path, path_flow))  # Store path and flow
            max_flow += path_flow
            v = sink
            while v != source:
                u = parent[v]
                self.flow[u][v] += path_flow
                self.flow[v][u] -= path_flow
                v = parent[v]
        
        return max_flow

    def print_paths(self):
        for path, flow in self.paths:
            print(f"Path with flow {flow}: {' -> '.join([f'{u}->{v}' for u, v in path])}")

# Initialize graph
g = Graph()
g.add_edge('E', 'a', 5, 5)
g.add_edge('E', 'c', 8, 8)
g.add_edge('E', 'b', 10, 10)
g.add_edge('a', 'd', 7, 7)
g.add_edge('a', 'e', 10, 10)
g.add_edge('b', 'e', 2, 2)
g.add_edge('b', 'c', 1, 1)
g.add_edge('c', 'e', 2, 2)
g.add_edge('c', 'f', 4, 4)
g.add_edge('d', 'g', 7, 7)
g.add_edge('e', 'g', 4, 4)
g.add_edge('e', 'S', 6, 6)
g.add_edge('e', 'f', 2, 2)
g.add_edge('g', 'S', 10, 10)
g.add_edge('f', 'S', 6, 6)
# Compute the maximum flow from source S to sink R
max_flow = g.ford_fulkerson('E', 'S')
print(f"Maximum flow: {max_flow}")

# Print the paths used to achieve the maximum flow
g.print_paths()
