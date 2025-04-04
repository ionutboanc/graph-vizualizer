import math
import tkinter as tk

class Edge:
    def __init__(self, canvas, source, target, capacity):
        self.canvas = canvas
        self.source = source
        self.target = target
        self.capacity = capacity
        self.flow = 0
        
        x1, y1 = source.x, source.y
        x2, y2 = target.x, target.y
        
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        
        if length > 0:
            dx, dy = dx/length, dy/length
            
            start_x = x1 + dx * source.radius
            start_y = y1 + dy * source.radius
            end_x = x2 - dx * target.radius
            end_y = y2 - dy * target.radius
            
            self.line = canvas.create_line(
                start_x, start_y, end_x, end_y,
                arrow=tk.LAST, fill="black", tags="edge"
            )
            
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            
            if abs(dx) < 0.1:
                if dy > 0:
                    offset_x = 15
                    offset_y = 0
                else:
                    offset_x = 15
                    offset_y = 0
            else:
                offset_x = dy * 10
                offset_y = -dx * 10
            
            self.label = canvas.create_text(
                mid_x + offset_x, mid_y + offset_y, 
                text=str(capacity), 
                font=("Arial", 9), 
                tags="edge_label"
            )
    
    def update_label(self, show_flow=False):
        if show_flow:
            text = f"{self.flow}/{self.capacity}"
        else:
            text = str(self.capacity)
        
        self.canvas.itemconfig(self.label, text=text)
        
    def set_color(self, color, width=1):
        self.canvas.itemconfig(self.line, fill=color, width=width)
        
    def delete(self):
        self.canvas.delete(self.line)
        self.canvas.delete(self.label)