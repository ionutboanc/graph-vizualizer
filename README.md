# 🔀 Graph Visualizer

Graph Visualizer is a desktop application that shows, step by step, how different algorithms find the maximum flow through a network. Users draw their own network on screen, choose a start and end point, and watch each algorithm work through the problem in real time.

It is a solo university project, built in April 2025.

## 💡 Why Graph Visualizer

Maximum flow is a classic problem in computer science. It answers questions like how much water can move through a set of pipes, how much traffic a road network can handle, or how much data can travel across a computer network at once. There are many algorithms that solve it, but on paper they can be hard to follow and even harder to compare.

Graph Visualizer turns these algorithms into something you can see. Instead of reading through pages of theory, users build a network, run an algorithm and follow every step as it happens. Running several algorithms on the same network makes it easy to understand how each one thinks and why some reach the answer faster than others.

## ✨ What it does

🖱️ **Draw a network.** Click anywhere on the canvas to add a point, then connect points with arrows to create routes between them.

⚙️ **Set capacities.** Each route can be given a capacity, which is the maximum amount that can pass through it, in either direction.

🎯 **Choose a start and end.** Mark one point as the source, where the flow begins, and another as the sink, where it ends. A color legend keeps everything easy to read.

▶️ **Watch it run.** As an algorithm works, the route it is currently using is highlighted and the flow on each connection is updated live. Routes that are completely full are greyed out.

📈 **See the result.** When the algorithm finishes, the maximum flow is shown in the status bar, so results from different algorithms can be compared side by side.

## 🧠 Algorithms included

The app includes seven maximum flow algorithms, from the most basic approach to more advanced ones:

| Algorithm | Button |
|---|---|
| Generic augmenting path | Generic |
| Ford-Fulkerson | FF |
| Edmonds-Karp | EK |
| Ahuja-Orlin | AO |
| Gabow (capacity scaling) | Gabow |
| Ahuja-Orlin shortest path | AODS |
| Ahuja-Orlin layered network | AORS |

## 🛠️ How it was built

Graph Visualizer is written in Python and uses Tkinter, Python's built-in toolkit for desktop interfaces. All of the algorithms were implemented from scratch, without relying on any graph libraries. It needs no installation beyond Python itself.

## ▶️ Try it

With Python 3 installed, run:

```
python app.py
```
