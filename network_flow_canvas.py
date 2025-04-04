import math
import tkinter as tk
from tkinter import messagebox
from node import Node
from edge import Edge
from flow_algorithms import Graph, edmonds_karp, ford_fulkerson, generic_flow_algorithm

class NetworkFlowCanvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.G = Graph()
        
        self.nodes = {}
        self.edges = {}
        self.selected_node = None
        self.source_node = None
        self.sink_node = None
        self.next_node_id = 1
        
        self.forward_capacity = 1
        self.backward_capacity = 0
        
        self.bind("<Button-1>", self.on_canvas_click)
        
        self.create_legend()
    
    def create_legend(self):
        y_pos = 20
        for color, text in [
            ("#00FF00", "Source"),
            ("#FF0000", "Sink"),
            ("#FFA500", "Selected"),
            ("lightblue", "Regular Node")
        ]:
            self.create_rectangle(20, y_pos, 40, y_pos + 20, fill=color, outline="black")
            self.create_text(50, y_pos + 10, text=text, anchor=tk.W)
            y_pos += 30
    
    def on_canvas_click(self, event):
        for node_id, node in self.nodes.items():
            dx = event.x - node.x
            dy = event.y - node.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance <= node.radius:
                return
        
        self.create_node(event.x, event.y)
    
    def create_node(self, x, y):
        node_id = self.next_node_id
        self.next_node_id += 1
        
        self.G.add_node(node_id)
        
        node = Node(self, node_id, x, y)
        self.nodes[node_id] = node
        
        return node
    
    def create_edge(self, source_id, target_id, forward_capacity, backward_capacity):
        self.G.add_edge(source_id, target_id, forward_capacity)
        
        edge = Edge(self, self.nodes[source_id], self.nodes[target_id], forward_capacity)
        self.edges[(source_id, target_id)] = edge
        
        if backward_capacity > 0:
            self.G.add_edge(target_id, source_id, backward_capacity)
            back_edge = Edge(self, self.nodes[target_id], self.nodes[source_id], backward_capacity)
            self.edges[(target_id, source_id)] = back_edge
    
    def set_capacity(self, forward, backward):
        self.forward_capacity = forward
        self.backward_capacity = backward
    
    def set_as_source(self):
        if self.selected_node is not None:
            if self.source_node is not None and self.source_node != self.sink_node:
                self.source_node.set_color("lightblue")
            
            self.source_node = self.selected_node
            self.source_node.set_color("#00FF00")
            
            self.selected_node = None
    
    def set_as_sink(self):
        if self.selected_node is not None:
            if self.sink_node is not None and self.sink_node != self.source_node:
                self.sink_node.set_color("lightblue")
            
            self.sink_node = self.selected_node
            self.sink_node.set_color("#FF0000")
            
            self.selected_node = None
            
    def select_node(self, node_id):
        clicked_node = self.nodes.get(node_id)
        
        if clicked_node:
            if self.selected_node is None:
                self.selected_node = clicked_node
                clicked_node.set_color("#FFA500")
            else:
                if self.selected_node.node_id != node_id:
                    self.create_edge(
                        self.selected_node.node_id, 
                        node_id, 
                        self.forward_capacity, 
                        self.backward_capacity
                    )
                
                if self.selected_node != self.source_node and self.selected_node != self.sink_node:
                    self.selected_node.set_color("lightblue")
                self.selected_node = None
    
    def calculate_generic(self):
        if self.source_node is not None and self.sink_node is not None:
            try:
                for edge in self.edges.values():
                    edge.flow = 0
                    edge.update_label()
                    edge.set_color("black", 1)
                
                def update_visualization(flow_graph, path, path_flow):
                    for edge in self.edges.values():
                        edge.set_color("black", 1)
                    
                    for (u, v), edge in self.edges.items():
                        if u in flow_graph.edges and v in flow_graph.edges[u]:
                            edge.flow = flow_graph.edges[u][v]['flow']
                            edge.capacity = flow_graph.edges[u][v]['capacity']
                            edge.update_label(show_flow=True)
                            
                            if edge.flow == edge.capacity and edge.capacity > 0:
                                edge.set_color("gray", 0.5)
                    
                    if path and len(path) > 1:
                        for i in range(len(path) - 1):
                            u, v = path[i], path[i+1]
                            if (u, v) in self.edges:
                                self.edges[(u, v)].set_color("#FF00FF", 3)
                    
                    self.update()
                    self.after(10000)
                
                max_flow, _ = generic_flow_algorithm(
                    self.G, 
                    self.source_node.node_id,
                    self.sink_node.node_id,
                    update_visualization
                )
                
                return max_flow
                
            except Exception as e:
                messagebox.showerror("Error", f"Error calculating flow: {e}")
        
        return 0

    def calculate_ford_fulkerson(self):
        if self.source_node is not None and self.sink_node is not None:
            try:
                for edge in self.edges.values():
                    edge.flow = 0
                    edge.update_label()
                    edge.set_color("black", 1)
                
                def update_visualization(flow_graph, path, path_flow):
                    for edge in self.edges.values():
                        edge.set_color("black", 1)
                    
                    for (u, v), edge in self.edges.items():
                        if u in flow_graph.edges and v in flow_graph.edges[u]:
                            edge.flow = flow_graph.edges[u][v]['flow']
                            edge.capacity = flow_graph.edges[u][v]['capacity']
                            edge.update_label(show_flow=True)
                            
                            if edge.flow == edge.capacity and edge.capacity > 0:
                                edge.set_color("gray", 0.5)
                    
                    if path and len(path) > 1:
                        for i in range(len(path) - 1):
                            u, v = path[i], path[i+1]
                            if (u, v) in self.edges:
                                self.edges[(u, v)].set_color("#FF00FF", 3)
                    
                    self.update()
                    self.after(10000)
                    
                    if path and len(path) > 1:
                        for i in range(len(path) - 1):
                            u, v = path[i], path[i+1]
                            if (u, v) in self.edges:
                                self.edges[(u, v)].set_color("black", 1)
                
                max_flow, _ = ford_fulkerson(
                    self.G, 
                    self.source_node.node_id,
                    self.sink_node.node_id,
                    update_visualization
                )
                
                return max_flow
                
            except Exception as e:
                messagebox.showerror("Error", f"Error calculating flow: {e}")
        
        return 0

    def calculate_edmonds_karp(self):
        if self.source_node is not None and self.sink_node is not None:
            try:
                for edge in self.edges.values():
                    edge.flow = 0
                    edge.update_label()
                    edge.set_color("black", 1)
                
                def update_visualization(flow_graph, path, path_flow):
                    for edge in self.edges.values():
                        edge.set_color("black", 1)
                    
                    for (u, v), edge in self.edges.items():
                        if u in flow_graph.edges and v in flow_graph.edges[u]:
                            edge.flow = flow_graph.edges[u][v]['flow']
                            edge.capacity = flow_graph.edges[u][v]['capacity']
                            edge.update_label(show_flow=True)
                            
                            if edge.flow == edge.capacity and edge.capacity > 0:
                                edge.set_color("gray", 0.5)
                    
                    if path and len(path) > 1:
                        for i in range(len(path) - 1):
                            u, v = path[i], path[i+1]
                            if (u, v) in self.edges:
                                self.edges[(u, v)].set_color("#FF00FF", 3)
                    
                    self.update()
                    self.after(10000)
                    
                    if path and len(path) > 1:
                        for i in range(len(path) - 1):
                            u, v = path[i], path[i+1]
                            if (u, v) in self.edges:
                                self.edges[(u, v)].set_color("black", 1)
                
                max_flow, _ = edmonds_karp(
                    self.G, 
                    self.source_node.node_id,
                    self.sink_node.node_id,
                    update_visualization
                )
                
                return max_flow
                
            except Exception as e:
                messagebox.showerror("Error", f"Error calculating flow: {e}")
        
        return 0