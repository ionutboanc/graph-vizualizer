import tkinter as tk
from tkinter import ttk, messagebox
from network_flow_canvas import NetworkFlowCanvas

class NetworkFlowApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Network Flow Visualization')
        self.geometry('1000x600')
        
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = NetworkFlowCanvas(main_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(controls_frame, text='Forward Capacity:').pack(side=tk.LEFT, padx=5)
        self.forward_input = ttk.Entry(controls_frame, width=5)
        self.forward_input.insert(0, '1')
        self.forward_input.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(controls_frame, text='Backward Capacity:').pack(side=tk.LEFT, padx=5)
        self.backward_input = ttk.Entry(controls_frame, width=5)
        self.backward_input.insert(0, '0')
        self.backward_input.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_frame, text='Set Source', command=self.set_as_source).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text='Set Sink', command=self.set_as_sink).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text='Generic', command=self.calculate_generic).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text='Ford-Fulkerson', command=self.calculate_ford_fulkerson).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text='Edmonds-Karp', command=self.calculate_edmonds_karp).pack(side=tk.LEFT, padx=5)
        
        self.status_var = tk.StringVar()
        self.status_var.set('Ready')
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        instructions = ttk.Label(main_frame, text="Click to add nodes. Select a node then click another to connect. Use buttons to set source/sink.")
        instructions.pack(pady=5)
        
        self.forward_input.bind("<KeyRelease>", self.update_capacities)
        self.backward_input.bind("<KeyRelease>", self.update_capacities)
        
        self.update_capacities(None)
    
    def update_capacities(self, event):
        try:
            forward = int(self.forward_input.get() or "1")
            backward = int(self.backward_input.get() or "0")
            self.canvas.set_capacity(forward, backward)
        except ValueError:
            self.status_var.set('Capacity must be an integer')
    
    def set_as_source(self):
        self.canvas.set_as_source()
    
    def set_as_sink(self):
        self.canvas.set_as_sink()
    
    def calculate_generic(self):
        flow = self.canvas.calculate_generic()
        self.status_var.set(f"Maximum Flow (Generic): {flow}")
    
    def calculate_ford_fulkerson(self):
        flow = self.canvas.calculate_ford_fulkerson()
        self.status_var.set(f"Maximum Flow (Ford-Fulkerson): {flow}")

    def calculate_edmonds_karp(self):
        flow = self.canvas.calculate_edmonds_karp()
        self.status_var.set(f"Maximum Flow (Edmonds-Karp): {flow}")

if __name__ == '__main__':
    app = NetworkFlowApp()
    app.mainloop()