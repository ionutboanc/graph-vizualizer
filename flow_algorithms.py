from collections import deque
import random

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
    
    def add_node(self, node):
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = {}
    
    def add_edge(self, u, v, capacity):
        self.add_node(u)
        self.add_node(v)
        self.edges[u][v] = {'capacity': capacity, 'flow': 0}
        if v not in self.edges:
            self.edges[v] = {}
        if u not in self.edges[v]:
            self.edges[v][u] = {'capacity': 0, 'flow': 0}
    
    def get_residual_capacity(self, u, v):
        if v in self.edges[u]:
            if self.edges[u][v]['capacity'] > 0:
                return self.edges[u][v]['capacity'] - self.edges[u][v]['flow']
            else:
                return self.edges[v][u]['flow']
        return 0

    def augment_flow(self, u, v, amount):
        if self.edges[u][v]['capacity'] > 0:
            self.edges[u][v]['flow'] += amount
        else:
            self.edges[v][u]['flow'] -= amount

def generic_flow_algorithm(graph, source, sink, callback=None):
    flow_graph = Graph()
    for u in graph.edges:
        for v in graph.edges[u]:
            flow_graph.add_edge(u, v, graph.edges[u][v]['capacity'])
    
    max_flow = 0
    
    while True:
        path = [source]
        visited = {source}
        current = source
        found_path = False
        
        while current != sink:
            valid_neighbors = [v for v in flow_graph.edges[current] 
                             if v not in visited and flow_graph.get_residual_capacity(current, v) > 0]
            
            if not valid_neighbors:
                if len(path) > 1:
                    visited.add(current)
                    path.pop()
                    current = path[-1]
                    continue
                else:
                    break
            
            next_node = random.choice(valid_neighbors)
            path.append(next_node)
            visited.add(next_node)
            current = next_node
            
            if current == sink:
                found_path = True
                break
        
        if not found_path:
            break
        
        path_flow = float('inf')
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            path_flow = min(path_flow, flow_graph.get_residual_capacity(u, v))
        
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            flow_graph.augment_flow(u, v, path_flow)
        
        max_flow += path_flow
        
        if callback:
            callback(flow_graph, path, path_flow)
    
    return max_flow, flow_graph

def ford_fulkerson(graph, source, sink, callback=None):
    flow_graph = Graph()
    for u in graph.edges:
        for v in graph.edges[u]:
            flow_graph.add_edge(u, v, graph.edges[u][v]['capacity'])
    
    max_flow = 0
    
    while True:
        possible_first_steps = [v for v in flow_graph.edges[source] 
                              if flow_graph.get_residual_capacity(source, v) > 0]
        
        if not possible_first_steps:
            break
        
        random.shuffle(possible_first_steps)
        found_path = False
        
        for first_step in possible_first_steps:
            parent = {source: None, first_step: source}
            queue = deque([first_step])
            
            while queue and sink not in parent:
                u = queue.popleft()
                for v in flow_graph.edges[u]:
                    if v not in parent and flow_graph.get_residual_capacity(u, v) > 0:
                        parent[v] = u
                        queue.append(v)
            
            if sink in parent:
                found_path = True
                break
        
        if not found_path:
            break
        
        path = []
        v = sink
        while v is not None:
            path.append(v)
            v = parent.get(v)
        path.reverse()
        
        path_flow = float('inf')
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            path_flow = min(path_flow, flow_graph.get_residual_capacity(u, v))
        
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            flow_graph.augment_flow(u, v, path_flow)
        
        max_flow += path_flow
        
        if callback:
            callback(flow_graph, path, path_flow)
    
    return max_flow, flow_graph

def edmonds_karp(graph, source, sink, callback=None):
    flow_graph = Graph()
    for u in graph.edges:
        for v in graph.edges[u]:
            flow_graph.add_edge(u, v, graph.edges[u][v]['capacity'])
    
    max_flow = 0
    
    while True:
        parent = {source: None}
        queue = deque([source])
        
        while queue and sink not in parent:
            u = queue.popleft()
            for v in flow_graph.edges[u]:
                if v not in parent and flow_graph.get_residual_capacity(u, v) > 0:
                    parent[v] = u
                    queue.append(v)
        
        if sink not in parent:
            break
        
        if callback:
            path = []
            v = sink
            while v is not None:
                path.append(v)
                v = parent.get(v)
            path.reverse()
        
        v = sink
        path_flow = float('inf')
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, flow_graph.get_residual_capacity(u, v))
            v = u
        
        v = sink
        while v != source:
            u = parent[v]
            flow_graph.augment_flow(u, v, path_flow)
            v = u
        
        max_flow += path_flow
        
        if callback and 'path' in locals():
            callback(flow_graph, path, path_flow)
    
    return max_flow, flow_graph