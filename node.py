import tkinter as tk

class Node:
    def __init__(self, canvas, node_id, x, y, radius=20):
        self.canvas = canvas
        self.node_id = node_id
        self.x = x
        self.y = y
        self.radius = radius
        
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

    def set_color(self, color):
        self.canvas.itemconfig(self.circle, fill=color)
    
    def get_position(self):
        return (self.x, self.y)
    
    def delete(self):
        self.canvas.delete(self.circle)
        self.canvas.delete(self.label)