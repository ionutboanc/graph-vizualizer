from collections import deque
import random
import math

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

def ahuja_orlin(graph, source, sink, callback=None):

    flow_graph = Graph()
    for u in graph.edges:
        for v in graph.edges[u]:
            flow_graph.add_edge(u, v, graph.edges[u][v]['capacity'])
    
    max_capacity = 0
    for u in flow_graph.edges:
        for v in flow_graph.edges[u]:
            max_capacity = max(max_capacity, flow_graph.edges[u][v]['capacity'])
    
    r = 2 ** math.floor(math.log(max_capacity, 2))
    
    max_flow = 0
    
    while r >= 1:
        while True:
            parent = {source: None}
            queue = deque([source])
            
            while queue and sink not in parent:
                u = queue.popleft()
                for v in flow_graph.edges[u]:
                    if v not in parent and flow_graph.get_residual_capacity(u, v) >= r:
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
        
        r //= 2
    
    return max_flow, flow_graph

def gabow(graph, source, sink, callback=None):
    original_graph = Graph()
    for u in graph.edges:
        for v in graph.edges[u]:
            original_graph.add_edge(u, v, graph.edges[u][v]['capacity'])
    
    scaled_graphs = [original_graph]
    
    if callback:
        callback(original_graph, [], 0)
    
    k = 0
    max_flow = 0
    while True:
        next_graph = Graph()
        current_graph = scaled_graphs[k]
        has_augmenting_paths = False
        
        for u in current_graph.edges:
            for v in current_graph.edges[u]:
                capacity = current_graph.edges[u][v]['capacity']
                if capacity > 0:
                    next_capacity = capacity // 2
                    next_graph.add_edge(u, v, next_capacity)
                    if next_capacity > 0:
                        has_augmenting_paths = True
    
        
        if not has_augmenting_paths:
            break
            
        scaled_graphs.append(next_graph)
        k += 1
        
        if callback:
            callback(next_graph, [], 0)
    
    flow_solution = Graph()
    for node in graph.nodes:
        flow_solution.add_node(node)
    
    while k >= 0:
        current_graph = scaled_graphs[k]
        flow_graph = Graph()
        
        for node in current_graph.nodes:
            flow_graph.add_node(node)
            
        for u in current_graph.edges:
            for v in current_graph.edges[u]:
                flow_graph.add_edge(u, v, current_graph.edges[u][v]['capacity'])
        
        if callback:
            callback(flow_graph, [], 0)
        
        if k < len(scaled_graphs) - 1:
            for u in flow_solution.edges:
                for v in flow_solution.edges[u]:
                    if flow_solution.edges[u][v]['flow'] > 0:
                        doubled_flow = flow_solution.edges[u][v]['flow'] * 2
                        if doubled_flow <= flow_graph.edges[u][v]['capacity']:
                            flow_graph.edges[u][v]['flow'] = doubled_flow
            
            if callback:
                callback(flow_graph, [], 0)
        
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
            
            if callback:
                callback(flow_graph, path, path_flow)
                
            max_flow += path_flow * 2 ** k
        
        if callback:
            callback(flow_graph, [], 0)
        
        flow_solution = flow_graph
        k -= 1
    
    if callback:
        callback(flow_solution, [], 0)
    
    return max_flow, flow_solution


def compute_distance_labels(flow_graph, sink, n):

    distance = {}
    for node in flow_graph.nodes:
        distance[node] = n
    distance[sink] = 0
    
    queue = deque([sink])
    while queue:
        v = queue.popleft()
        for u in flow_graph.nodes:
            if v in flow_graph.edges[u] and flow_graph.get_residual_capacity(u, v) > 0:
                if distance[u] == n:
                    distance[u] = distance[v] + 1
                    queue.append(u)
    
    return distance

def ahuja_orlin_shortest_path(graph, source, sink, callback=None):

    flow_graph = Graph()
    for u in graph.edges:
        for v in graph.edges[u]:
            flow_graph.add_edge(u, v, graph.edges[u][v]['capacity'])
    
    f = 0
    n = len(flow_graph.nodes)
    
    distance = compute_distance_labels(flow_graph, sink, n)
    
    if callback:
        callback(flow_graph, [], 0, distance)
    
    predecessor = {}
    
    x = source
    
    while distance[source] < n:
        admissible_found = False
        
        for next_node in flow_graph.edges[x]:
            if (flow_graph.get_residual_capacity(x, next_node) > 0 and 
                distance[x] == distance[next_node] + 1):
                # INAINTARE
                predecessor[next_node] = x
                x = next_node
                admissible_found = True
                

                if x == sink:
                    # MARIRE
                    path = []
                    node = sink
                    while node != source:
                        path.append(node)
                        node = predecessor[node]
                    path.append(source)
                    path.reverse()
                    
                    path_flow = float('inf')
                    for i in range(len(path) - 1):
                        u, v = path[i], path[i+1]
                        path_flow = min(path_flow, flow_graph.get_residual_capacity(u, v))
                    
                    for i in range(len(path) - 1):
                        u, v = path[i], path[i+1]
                        flow_graph.augment_flow(u, v, path_flow)
                    
                    f += path_flow
                    
                    if callback:
                        callback(flow_graph, path, path_flow)
                    
                    distance = compute_distance_labels(flow_graph, sink, n)
                    
                    if callback:
                        callback(flow_graph, [], 0, distance)
                    
                    x = source
                
                break
        
        if not admissible_found:
            # INAPOIERE
            min_dist = n
            for next_node in flow_graph.edges[x]:
                if flow_graph.get_residual_capacity(x, next_node) > 0:
                    min_dist = min(min_dist, distance[next_node] + 1)

            if callback:
                callback(flow_graph, [], 0, distance)
            
            if x != source:
                x = predecessor[x]
    
    return f, flow_graph

def ahuja_orlin_stratified(graph, source, sink, callback=None):
    flow_graph = Graph()
    for u in graph.edges:
        for v in graph.edges[u]:
            flow_graph.add_edge(u, v, graph.edges[u][v]['capacity'])
    
    f = 0
    n = len(flow_graph.nodes)
    
    distance = compute_distance_labels(flow_graph, sink, n)
    
    if callback:
        callback(flow_graph, [], 0, distance)
    
    B = {node: 1 for node in flow_graph.nodes}
    
    predecessor = {}
    
    x = source
    
    while distance[source] < n:
        if B[source] == 1:
            admissible_found = False
            
            for y in flow_graph.edges[x]:
                if (flow_graph.get_residual_capacity(x, y) > 0 and 
                    distance[x] == distance[y] + 1 and 
                    B[y] == 1):
                    
                    # INAINTARE
                    predecessor[y] = x
                    x = y
                    admissible_found = True
                    
                    if x == sink:
                        # MARIRE
                        path = []
                        node = sink
                        while node != source:
                            path.append(node)
                            node = predecessor[node]
                        path.append(source)
                        path.reverse()
                        
                        path_flow = float('inf')
                        for i in range(len(path) - 1):
                            u, v = path[i], path[i+1]
                            path_flow = min(path_flow, flow_graph.get_residual_capacity(u, v))
                        
                        for i in range(len(path) - 1):
                            u, v = path[i], path[i+1]
                            flow_graph.augment_flow(u, v, path_flow)
                        
                        f += path_flow
                        
                        if callback:
                            callback(flow_graph, path, path_flow, distance)
                        
                        x = source
                    
                    break
            
            if not admissible_found:
                # INAPOIERE
                B[x] = 0
                
                if callback:
                    callback(flow_graph, [], 0, distance, B)
                
                if x != source:
                    x = predecessor[x]
        else:
            distance = compute_distance_labels(flow_graph, sink, n)
            B = {node: 1 for node in flow_graph.nodes}
            x = source
            
            if callback:
                callback(flow_graph, [], 0, distance, B)
    
    return f, flow_graph