import time
import random
import tkinter as tk
from tkinter import ttk, messagebox


# --- Core Algorithms ---

def interpolation_search(arr, target):
    """
    Interpolation Search Algorithm
    Time Complexity: O(log log n) average, O(n) worst case
    Space Complexity: O(1)
    """
    low, high = 0, len(arr) - 1
    comparisons = 0
    trace = []

    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1
        if low == high:
            if arr[low] == target:
                trace.append((low, comparisons, "Found target"))
                return low, comparisons, trace
            trace.append((low, comparisons, "Target not found"))
            return -1, comparisons, trace

        # Interpolation formula
        pos = low + int(((target - arr[low]) * (high - low)) / (arr[high] - arr[low]))
        trace.append((pos, comparisons, f"Probing index {pos}"))

        if arr[pos] == target:
            return pos, comparisons, trace
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1, comparisons, trace


def binary_search(arr, target):
    """Binary Search Algorithm"""
    low, high = 0, len(arr) - 1
    comparisons = 0
    trace = []

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        trace.append((mid, comparisons, f"Mid index {mid}"))

        if arr[mid] == target:
            return mid, comparisons, trace
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons, trace


# --- Tkinter GUI Interface ---

class SearchBenchmarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Visualizer: Interpolation vs Binary Search")
        self.root.geometry("900x650")
        self.root.minsize(800, 550)

        # Color Palette
        self.colors = {
            "bg": "#1e1e2e",
            "card": "#252538",
            "accent": "#89b4fa",
            "accent_hover": "#b4befe",
            "text": "#cdd6f4",
            "subtext": "#a6adc8",
            "success": "#a6e3a1",
            "danger": "#f38ba8",
            "highlight": "#f9e2af",
            "list_bg": "#181825"
        }

        self.root.configure(bg=self.colors["bg"])
        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Tab notebook styling
        self.style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        self.style.configure(
            "TNotebook.Tab",
            background=self.colors["card"],
            foreground=self.colors["subtext"],
            padding=[15, 8],
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", self.colors["accent"])],
            foreground=[("selected", "#11111b")]
        )

        # Treeview (Table) Styling
        self.style.configure(
            "Treeview",
            background=self.colors["list_bg"],
            foreground=self.colors["text"],
            fieldbackground=self.colors["list_bg"],
            rowheight=28,
            font=("Segoe UI", 10)
        )
        self.style.configure(
            "Treeview.Heading",
            background=self.colors["card"],
            foreground=self.colors["accent"],
            font=("Segoe UI", 10, "bold")
        )
        self.style.map("Treeview", background=[("selected", self.colors["card"])])

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=15, padx=25)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Algorithm Performance & Visualization Tool",
            font=("Segoe UI", 18, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Interpolation Search O(log log n) vs Binary Search O(log n)",
            font=("Segoe UI", 10),
            fg=self.colors["subtext"],
            bg=self.colors["bg"]
        ).pack(anchor="w")

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        # Tab 1: Single Search Visualizer
        self.tab_visualizer = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(self.tab_visualizer, text="Interactive Search")
        self._build_visualizer_tab()

        # Tab 2: Performance Benchmark
        self.tab_benchmark = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(self.tab_benchmark, text="Performance Analysis")
        self._build_benchmark_tab()

    def _build_visualizer_tab(self):
        # Input Controls
        ctrl_frame = tk.Frame(self.tab_visualizer, bg=self.colors["card"], padx=15, pady=15)
        ctrl_frame.pack(fill="x", pady=10)

        # Array Entry
        tk.Label(
            ctrl_frame, text="Sorted Array (comma-separated):",
            font=("Segoe UI", 9, "bold"), fg=self.colors["subtext"], bg=self.colors["card"]
        ).grid(row=0, column=0, sticky="w", padx=5)

        self.array_entry = tk.Entry(
            ctrl_frame, bg=self.colors["list_bg"], fg=self.colors["text"],
            insertbackground=self.colors["text"], relief="flat", font=("Segoe UI", 10), width=45
        )
        self.array_entry.grid(row=0, column=1, padx=5, pady=5)
        self.array_entry.insert(0, "2, 5, 10, 15, 23, 35, 48, 60, 75, 90, 105, 120")

        # Target Entry
        tk.Label(
            ctrl_frame, text="Target Value:",
            font=("Segoe UI", 9, "bold"), fg=self.colors["subtext"], bg=self.colors["card"]
        ).grid(row=0, column=2, sticky="w", padx=(15, 5))

        self.target_entry = tk.Entry(
            ctrl_frame, bg=self.colors["list_bg"], fg=self.colors["text"],
            insertbackground=self.colors["text"], relief="flat", font=("Segoe UI", 10), width=10
        )
        self.target_entry.grid(row=0, column=3, padx=5, pady=5)
        self.target_entry.insert(0, "35")

        # Run Button
        run_btn = tk.Button(
            ctrl_frame, text="Execute Search", font=("Segoe UI", 10, "bold"),
            bg=self.colors["accent"], fg="#11111b", activebackground=self.colors["accent_hover"],
            relief="flat", cursor="hand2", command=self.run_single_search
        )
        run_btn.grid(row=0, column=4, padx=(15, 5), ipady=3)

        # Output Cards Area
        output_frame = tk.Frame(self.tab_visualizer, bg=self.colors["bg"])
        output_frame.pack(fill="both", expand=True, pady=10)

        # Interpolation Results Panel
        is_box = tk.LabelFrame(
            output_frame, text=" Interpolation Search ",
            font=("Segoe UI", 10, "bold"), fg=self.colors["accent"], bg=self.colors["card"], padx=10, pady=10
        )
        is_box.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.is_result_lbl = tk.Label(
            is_box, text="Result: Waiting...", font=("Segoe UI", 10, "bold"),
            fg=self.colors["text"], bg=self.colors["card"], anchor="w"
        )
        self.is_result_lbl.pack(fill="x", pady=(0, 5))

        self.is_trace_list = tk.Listbox(
            is_box, bg=self.colors["list_bg"], fg=self.colors["text"],
            font=("Consolas", 10), relief="flat", highlightthickness=0
        )
        self.is_trace_list.pack(fill="both", expand=True)

        # Binary Results Panel
        bs_box = tk.LabelFrame(
            output_frame, text=" Binary Search ",
            font=("Segoe UI", 10, "bold"), fg=self.colors["accent"], bg=self.colors["card"], padx=10, pady=10
        )
        bs_box.pack(side="right", fill="both", expand=True, padx=(5, 0))

        self.bs_result_lbl = tk.Label(
            bs_box, text="Result: Waiting...", font=("Segoe UI", 10, "bold"),
            fg=self.colors["text"], bg=self.colors["card"], anchor="w"
        )
        self.bs_result_lbl.pack(fill="x", pady=(0, 5))

        self.bs_trace_list = tk.Listbox(
            bs_box, bg=self.colors["list_bg"], fg=self.colors["text"],
            font=("Consolas", 10), relief="flat", highlightthickness=0
        )
        self.bs_trace_list.pack(fill="both", expand=True)

    def _build_benchmark_tab(self):
        top_bar = tk.Frame(self.tab_benchmark, bg=self.colors["bg"])
        top_bar.pack(fill="x", pady=10)

        bench_btn = tk.Button(
            top_bar, text="▶ Run Performance Benchmark", font=("Segoe UI", 10, "bold"),
            bg=self.colors["success"], fg="#11111b", relief="flat", cursor="hand2",
            command=self.run_benchmark
        )
        bench_btn.pack(side="left", ipady=5, ipadx=10)

        self.bench_status = tk.Label(
            top_bar, text="Click to benchmark over array sizes [1000 to 100,000]",
            font=("Segoe UI", 9), fg=self.colors["subtext"], bg=self.colors["bg"]
        )
        self.bench_status.pack(side="left", padx=15)

        # Table Layout
        table_frame = tk.Frame(self.tab_benchmark, bg=self.colors["card"])
        table_frame.pack(fill="both", expand=True, pady=5)

        columns = ("size", "is_time", "bs_time", "is_comp", "bs_comp")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("size", text="Array Size")
        self.tree.heading("is_time", text="IS Time (ms)")
        self.tree.heading("bs_time", text="BS Time (ms)")
        self.tree.heading("is_comp", text="IS Comparisons")
        self.tree.heading("bs_comp", text="BS Comparisons")

        self.tree.column("size", anchor="center", width=120)
        self.tree.column("is_time", anchor="center", width=140)
        self.tree.column("bs_time", anchor="center", width=140)
        self.tree.column("is_comp", anchor="center", width=150)
        self.tree.column("bs_comp", anchor="center", width=150)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def run_single_search(self):
        try:
            arr = [int(x.strip()) for x in self.array_entry.get().split(",")]
            target = int(self.target_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please ensure numbers are correctly entered.")
            return

        # Check if array is sorted
        if arr != sorted(arr):
            messagebox.showwarning("Unsorted Array", "Array must be sorted for search algorithms to function correctly.")
            return

        # Run Interpolation
        idx_is, comp_is, trace_is = interpolation_search(arr, target)
        self.is_trace_list.delete(0, tk.END)
        if idx_is != -1:
            self.is_result_lbl.config(text=f"Found at Index: {idx_is} | Comparisons: {comp_is}", fg=self.colors["success"])
        else:
            self.is_result_lbl.config(text=f"Not Found | Comparisons: {comp_is}", fg=self.colors["danger"])

        for step in trace_is:
            self.is_trace_list.insert(tk.END, f" Step {step[1]}: {step[2]}")

        # Run Binary
        idx_bs, comp_bs, trace_bs = binary_search(arr, target)
        self.bs_trace_list.delete(0, tk.END)
        if idx_bs != -1:
            self.bs_result_lbl.config(text=f"Found at Index: {idx_bs} | Comparisons: {comp_bs}", fg=self.colors["success"])
        else:
            self.bs_result_lbl.config(text=f"Not Found | Comparisons: {comp_bs}", fg=self.colors["danger"])

        for step in trace_bs:
            self.bs_trace_list.insert(tk.END, f" Step {step[1]}: {step[2]}")

    def run_benchmark(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.bench_status.config(text="Running benchmark tests... please wait.")
        self.root.update_idletasks()

        sizes = [1000, 5000, 10000, 50000, 100000]

        for size in sizes:
            arr = sorted(random.sample(range(size * 10), size))
            target = arr[random.randint(0, size - 1)]

            # Interpolation timing
            start = time.perf_counter()
            for _ in range(100):
                idx_is, comp_is, _ = interpolation_search(arr, target)
            is_time = (time.perf_counter() - start) / 100 * 1000

            # Binary timing
            start = time.perf_counter()
            for _ in range(100):
                idx_bs, comp_bs, _ = binary_search(arr, target)
            bs_time = (time.perf_counter() - start) / 100 * 1000

            # Insert into Treeview
            self.tree.insert(
                "", tk.END,
                values=(f"{size:,}", f"{is_time:.4f}", f"{bs_time:.4f}", comp_is, comp_bs)
            )

        self.bench_status.config(text="Benchmark complete!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SearchBenchmarkApp(root)
    root.mainloop()
