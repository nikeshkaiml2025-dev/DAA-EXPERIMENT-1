import time
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox


# --- Algorithm Implementations ---

def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    matches, comparisons = [], 0
    if m == 0 or n < m:
        return matches, comparisons

    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)
    return matches, comparisons


def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length, i = 0, 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0 or n < m:
        return [], 0
    lps = compute_lps(pattern)
    matches, comparisons = [], 0
    i = j = 0
    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches, comparisons


def rabin_karp(text, pattern, q=101):
    n, m = len(text), len(pattern)
    if m == 0 or n < m:
        return [], 0
    d = 256
    h = pow(d, m - 1, q)
    p_hash = t_hash = 0
    matches, comparisons = [], 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):
        if p_hash == t_hash:
            for k in range(m):
                comparisons += 1
                if text[s + k] != pattern[k]:
                    break
            else:
                matches.append(s)
        if s < n - m:
            t_hash = (d * (t_hash - ord(text[s]) * h) + ord(text[s + m])) % q
            if t_hash < 0:
                t_hash += q
    return matches, comparisons


# --- Tkinter Application ---

class PatternMatchingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pattern Matching Visualizer & Benchmark")
        self.root.geometry("920x680")
        self.root.minsize(820, 580)

        # Dark Theme Colors
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

        self.style.configure(
            "Treeview",
            background=self.colors["list_bg"],
            foreground=self.colors["text"],
            fieldbackground=self.colors["list_bg"],
            rowheight=30,
            font=("Segoe UI", 10)
        )
        self.style.configure(
            "Treeview.Heading",
            background=self.colors["card"],
            foreground=self.colors["accent"],
            font=("Segoe UI", 10, "bold")
        )

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=15, padx=25)
        header.pack(fill="x")

        tk.Label(
            header,
            text="String Pattern Matching Studio",
            font=("Segoe UI", 18, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Compare Naive, KMP, and Rabin-Karp Search Algorithms",
            font=("Segoe UI", 10),
            fg=self.colors["subtext"],
            bg=self.colors["bg"]
        ).pack(anchor="w")

        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        self.tab_visualizer = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(self.tab_visualizer, text="Interactive Matcher")

        self.tab_benchmark = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(self.tab_benchmark, text="Performance Comparison")

        self._build_visualizer_tab()
        self._build_benchmark_tab()

    def _build_visualizer_tab(self):
        # Input Section
        ctrl = tk.Frame(self.tab_visualizer, bg=self.colors["card"], padx=15, pady=15)
        ctrl.pack(fill="x", pady=10)

        # Text input
        tk.Label(ctrl, text="Source Text:", font=("Segoe UI", 9, "bold"), fg=self.colors["subtext"], bg=self.colors["card"]).grid(row=0, column=0, sticky="w", padx=5)
        self.text_entry = tk.Entry(ctrl, bg=self.colors["list_bg"], fg=self.colors["text"], insertbackground=self.colors["text"], relief="flat", font=("Consolas", 10), width=45)
        self.text_entry.grid(row=0, column=1, padx=5, pady=5)
        self.text_entry.insert(0, "AABAACAADAABAABA")

        # Pattern input
        tk.Label(ctrl, text="Pattern:", font=("Segoe UI", 9, "bold"), fg=self.colors["subtext"], bg=self.colors["card"]).grid(row=0, column=2, sticky="w", padx=(15, 5))
        self.pattern_entry = tk.Entry(ctrl, bg=self.colors["list_bg"], fg=self.colors["text"], insertbackground=self.colors["text"], relief="flat", font=("Consolas", 10), width=15)
        self.pattern_entry.grid(row=0, column=3, padx=5, pady=5)
        self.pattern_entry.insert(0, "AABA")

        run_btn = tk.Button(ctrl, text="Search All", font=("Segoe UI", 10, "bold"), bg=self.colors["accent"], fg="#11111b", relief="flat", cursor="hand2", command=self.run_interactive_search)
        run_btn.grid(row=0, column=4, padx=(15, 5), ipady=3)

        # Highlighted Output View
        view_frame = tk.LabelFrame(self.tab_visualizer, text=" Text Visualizer ", font=("Segoe UI", 10, "bold"), fg=self.colors["accent"], bg=self.colors["card"], padx=10, pady=10)
        view_frame.pack(fill="x", pady=10)

        self.text_display = tk.Text(view_frame, height=3, bg=self.colors["list_bg"], fg=self.colors["text"], font=("Consolas", 12), relief="flat", wrap="char")
        self.text_display.pack(fill="x")
        self.text_display.tag_configure("match", background="#313244", foreground=self.colors["success"], font=("Consolas", 12, "bold"))

        # Cards for Stats
        stats_frame = tk.Frame(self.tab_visualizer, bg=self.colors["bg"])
        stats_frame.pack(fill="both", expand=True, pady=10)

        self.cards = {}
        algos = [("Naive", "Naive Search"), ("KMP", "Knuth-Morris-Pratt"), ("RK", "Rabin-Karp")]
        for name, full_name in algos:
            box = tk.LabelFrame(stats_frame, text=f" {full_name} ", font=("Segoe UI", 10, "bold"), fg=self.colors["accent"], bg=self.colors["card"], padx=10, pady=10)
            box.pack(side="left", fill="both", expand=True, padx=4)

            lbl_matches = tk.Label(box, text="Matches at: -", font=("Segoe UI", 9), fg=self.colors["text"], bg=self.colors["card"], anchor="w", justify="left")
            lbl_matches.pack(fill="x", pady=2)

            lbl_comps = tk.Label(box, text="Comparisons: -", font=("Segoe UI", 10, "bold"), fg=self.colors["highlight"], bg=self.colors["card"], anchor="w")
            lbl_comps.pack(fill="x", pady=2)

            self.cards[name] = (lbl_matches, lbl_comps)

    def _build_benchmark_tab(self):
        top_bar = tk.Frame(self.tab_benchmark, bg=self.colors["bg"])
        top_bar.pack(fill="x", pady=10)

        bench_btn = tk.Button(top_bar, text="▶ Run Benchmark (Text Len: 10,000)", font=("Segoe UI", 10, "bold"), bg=self.colors["success"], fg="#11111b", relief="flat", cursor="hand2", command=self.run_benchmark)
        bench_btn.pack(side="left", ipady=5, ipadx=10)

        self.bench_status = tk.Label(top_bar, text="Click to run comparison on generated random text.", font=("Segoe UI", 9), fg=self.colors["subtext"], bg=self.colors["bg"])
        self.bench_status.pack(side="left", padx=15)

        table_frame = tk.Frame(self.tab_benchmark, bg=self.colors["card"])
        table_frame.pack(fill="both", expand=True, pady=5)

        columns = ("pattern", "naive", "kmp", "rk")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("pattern", text="Pattern")
        self.tree.heading("naive", text="Naive Comparisons")
        self.tree.heading("kmp", text="KMP Comparisons")
        self.tree.heading("rk", text="Rabin-Karp Comparisons")

        self.tree.column("pattern", anchor="center", width=150)
        self.tree.column("naive", anchor="center", width=180)
        self.tree.column("kmp", anchor="center", width=180)
        self.tree.column("rk", anchor="center", width=180)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def run_interactive_search(self):
        text = self.text_entry.get()
        pattern = self.pattern_entry.get()

        if not text or not pattern:
            messagebox.showwarning("Input Error", "Text and Pattern cannot be empty.")
            return

        # Execute searches
        m1, c1 = naive_search(text, pattern)
        m2, c2 = kmp_search(text, pattern)
        m3, c3 = rabin_karp(text, pattern)

        # Update cards
        self.cards["Naive"][0].config(text=f"Matches at: {m1}")
        self.cards["Naive"][1].config(text=f"Comparisons: {c1}")

        self.cards["KMP"][0].config(text=f"Matches at: {m2}")
        self.cards["KMP"][1].config(text=f"Comparisons: {c2}")

        self.cards["RK"][0].config(text=f"Matches at: {m3}")
        self.cards["RK"][1].config(text=f"Comparisons: {c3}")

        # Update highlighted text
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, text)

        pat_len = len(pattern)
        for idx in m1:
            start_pos = f"1.0 + {idx} chars"
            end_pos = f"1.0 + {idx + pat_len} chars"
            self.text_display.tag_add("match", start_pos, end_pos)

    def run_benchmark(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.bench_status.config(text="Benchmarking against random 10,000 char text...")
        self.root.update_idletasks()

        text_large = ''.join(random.choices('ABCD', k=10000))
        patterns = ['AB', 'ABCD', 'ABCDAB', 'ABCDABCD']

        for p in patterns:
            _, c1 = naive_search(text_large, p)
            _, c2 = kmp_search(text_large, p)
            _, c3 = rabin_karp(text_large, p)

            self.tree.insert("", tk.END, values=(p, f"{c1:,}", f"{c2:,}", f"{c3:,}"))

        self.bench_status.config(text="Benchmark completed!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PatternMatchingApp(root)
    root.mainloop()
