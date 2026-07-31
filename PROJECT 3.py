import tkinter as tk
from tkinter import messagebox
import heapq

# ------------------ Union Find ------------------

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


# ------------------ Kruskal ------------------

def kruskal(n, edges):

    edges.sort()

    uf = UnionFind(n)

    mst = []
    cost = 0

    for w, u, v in edges:

        if uf.union(u, v):

            mst.append((u, v, w))
            cost += w

            if len(mst) == n - 1:
                break

    return mst, cost


# ------------------ Prim ------------------

def prim(n, adj, start=0):

    INF = float("inf")

    key = [INF] * n
    parent = [-1] * n
    inMST = [False] * n

    key[start] = 0

    pq = [(0, start)]

    mst = []
    cost = 0

    while pq:

        w, u = heapq.heappop(pq)

        if inMST[u]:
            continue

        inMST[u] = True

        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w

        for v, wt in adj.get(u, []):

            if not inMST[v] and wt < key[v]:

                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))

    return mst, cost


# ------------------ Run Algorithm ------------------

def run_algorithm():

    try:
        n = int(vertex_entry.get())

        edge_text = edge_box.get("1.0", tk.END).strip()

        if edge_text == "":
            messagebox.showerror("Error", "Please enter graph edges.")
            return

        edges = []

        adj = {}

        for line in edge_text.split("\n"):

            w, u, v = map(int, line.split())

            edges.append((w, u, v))

            adj.setdefault(u, []).append((v, w))
            adj.setdefault(v, []).append((u, w))

        k_mst, k_cost = kruskal(n, edges[:])
        p_mst, p_cost = prim(n, adj)

        output.delete("1.0", tk.END)

        output.insert(tk.END, "========== KRUSKAL'S MST ==========\n\n")

        for u, v, w in k_mst:
            output.insert(
                tk.END,
                f"Edge ({u} - {v})    Weight = {w}\n"
            )

        output.insert(
            tk.END,
            f"\nTotal MST Cost : {k_cost}\n"
        )

        output.insert(
            tk.END,
            "\n====================================\n\n"
        )

        output.insert(
            tk.END,
            "=========== PRIM'S MST ============\n\n"
        )

        for u, v, w in p_mst:
            output.insert(
                tk.END,
                f"Edge ({u} - {v})    Weight = {w}\n"
            )

        output.insert(
            tk.END,
            f"\nTotal MST Cost : {p_cost}"
        )

    except Exception:
        messagebox.showerror(
            "Input Error",
            "Enter edges in the format:\n\nWeight Vertex1 Vertex2"
        )


# ------------------ Sample Graph ------------------

def load_sample():

    vertex_entry.delete(0, tk.END)
    vertex_entry.insert(0, "7")

    sample = """7 0 1
5 0 3
8 1 2
9 1 3
7 1 4
5 2 4
15 3 4
6 3 5
8 4 5
9 4 6
11 5 6"""

    edge_box.delete("1.0", tk.END)
    edge_box.insert(tk.END, sample)


# ------------------ Clear ------------------

def clear():

    vertex_entry.delete(0, tk.END)

    edge_box.delete("1.0", tk.END)

    output.delete("1.0", tk.END)


# ------------------ GUI ------------------

root = tk.Tk()

root.title("Minimum Spanning Tree Visualizer")
root.geometry("900x700")
root.configure(bg="#ECEFF1")

title = tk.Label(
    root,
    text="Minimum Spanning Tree (Kruskal vs Prim)",
    font=("Arial", 20, "bold"),
    bg="#ECEFF1",
    fg="darkblue"
)

title.pack(pady=10)

frame = tk.Frame(root, bg="#ECEFF1")
frame.pack()

tk.Label(
    frame,
    text="Number of Vertices",
    font=("Arial", 12, "bold"),
    bg="#ECEFF1"
).grid(row=0, column=0, sticky="w")

vertex_entry = tk.Entry(frame, width=10, font=("Arial", 12))
vertex_entry.grid(row=0, column=1, padx=10)

tk.Label(
    frame,
    text="Enter Edges (Weight Vertex1 Vertex2)",
    font=("Arial", 12, "bold"),
    bg="#ECEFF1"
).grid(row=1, column=0, columnspan=2, pady=10)

edge_box = tk.Text(frame, width=60, height=12, font=("Consolas", 11))
edge_box.grid(row=2, column=0, columnspan=2)

button_frame = tk.Frame(root, bg="#ECEFF1")
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="Load Sample",
    font=("Arial", 11, "bold"),
    bg="orange",
    fg="white",
    command=load_sample
).grid(row=0, column=0, padx=10)

tk.Button(
    button_frame,
    text="Find MST",
    font=("Arial", 11, "bold"),
    bg="green",
    fg="white",
    command=run_algorithm
).grid(row=0, column=1, padx=10)

tk.Button(
    button_frame,
    text="Clear",
    font=("Arial", 11, "bold"),
    bg="red",
    fg="white",
    command=clear
).grid(row=0, column=2, padx=10)

output = tk.Text(
    root,
    width=95,
    height=20,
    font=("Consolas", 11)
)

output.pack(pady=10)

load_sample()

root.mainloop()
