import tkinter as tk

class Node:
    def __init__(self, canvas, node_id, x, y, radius=20):
        self.canvas = canvas
        self.node_id = node_id
        self.x = x
        self.y = y
        self.radius = radius
        self.distance = None  # Initialize with None (no distance label)
        self.distance_text_id = None
        
        self.circle = canvas.create_oval(
            x - radius, y - radius, 
            x + radius, y + radius, 
            fill="lightblue", outline="black", width=2, tags=f"node_{node_id}"
        )
        
        self.label = canvas.create_text(
            x, y, text=str(node_id), font=("Arial", 10, "bold"), tags=f"node_{node_id}"
        )
        
        canvas.tag_bind(self.circle, "<Button-1>", lambda e, nid=node_id: canvas.select_node(nid))
        canvas.tag_bind(self.label, "<Button-1>", lambda e, nid=node_id: canvas.select_node(nid))
    
    def set_distance(self, distance):
        self.distance = distance
        self.update_distance_label()
    
    def update_distance_label(self):
            # Remove previous distance label if it exists
            if self.distance_text_id:
                self.canvas.delete(self.distance_text_id)
                
            # Create new distance label if distance is set
            if self.distance is not None:
                self.distance_text_id = self.canvas.create_text(
                    self.x, self.y + self.radius + 15,  # Position below the node
                    text=f"d:{self.distance}",
                    fill="blue",
                    font=("Arial", 10)
                )

    def set_color(self, color):
        self.canvas.itemconfig(self.circle, fill=color)
    
    def get_position(self):
        return (self.x, self.y)
    
    def delete(self):
        self.canvas.delete(self.circle)
        self.canvas.delete(self.label)