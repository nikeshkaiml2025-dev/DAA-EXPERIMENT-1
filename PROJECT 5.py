import random
import tkinter as tk
from tkinter import messagebox, ttk

# Initialize root window
root = tk.Tk()
root.title("Min-Max Algorithm Performance Dashboard")
root.geometry("900x720")
root.minsize(800, 650)
root.configure(bg="#0F172A")  # Slate 900 dark background

# Safe Theme Handling
style = ttk.Style()
available_themes = style.theme_names()

if "clamp" in available_themes:
    style.theme_use("clamp")
elif "default" in available_themes:
    style.theme_use("default")

# Color Palette Definitions
BG_DARK = "#0F172A"
CARD_BG = "#1E293B"
BORDER_COLOR = "#334155"
TEXT_LIGHT = "#F8FAFC"
TEXT_MUTED = "#94A3B8"
ACCENT_BLUE = "#38BDF8"
ACCENT_GREEN = "#34D399"
ACCENT_PURPLE = "#A78BFA"

# Widget Styling
style.configure("TFrame", background=BG_DARK)
style.configure(
    "Card.TFrame",
    background=CARD_BG,
    relief="flat",
    borderwidth=1,
)

style.configure(
    "TLabel", background=CARD_BG, foreground=TEXT_LIGHT, font=("Segoe UI", 10)
)
style.configure(
    "Header.TLabel",
    background=BG_DARK,
    foreground=TEXT_LIGHT,
    font=("Segoe UI", 16, "bold"),
)
style.configure(
    "SubHeader.TLabel",
    background=CARD_BG,
    foreground=ACCENT_BLUE,
    font=("Segoe UI", 12, "bold"),
)
style.configure(
    "Muted.TLabel",
    background=CARD_BG,
    foreground=TEXT_MUTED,
    font=("Segoe UI", 9),
)

# Treeview / Data Table Styling
style.configure(
    "Treeview",
    background=CARD_BG,
    foreground=TEXT_LIGHT,
    fieldbackground=CARD_BG,
    rowheight=32,
    font=("Segoe UI", 10),
    borderwidth=0,
)
style.configure(
    "Treeview.Heading",
    background="#090D16",
    foreground=ACCENT_BLUE,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
)
style.map("Treeview", background=[("selected", "#334155")])

# Custom Accent Button Styling
style.configure(
    "Accent.TButton",
    background=ACCENT_BLUE,
    foreground="#0F172A",
    font=("Segoe UI", 10, "bold"),
    borderwidth=0,
    focusthickness=0,
    padding=8,
)
style.map("Accent.TButton", background=[("active", "#7DD3FC")])

style.configure(
    "Secondary.TButton",
    background=BORDER_COLOR,
    foreground=TEXT_LIGHT,
    font=("Segoe UI", 9),
    borderwidth=0,
    padding=6,
)
style.map("Secondary.TButton", background=[("active", "#475569")])

# -------------------------------------------------------------------
# Algorithm Implementations
# -------------------------------------------------------------------
comparison_count = 0


def min_max_dc(arr, low, high):
    global comparison_count

    # Base case: single element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:
        comparison_count += 1
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2
    lmin, lmax = min_max_dc(arr, low, mid)
    rmin, rmax = min_max_dc(arr, mid + 1, high)

    # Conquer: combine with 2 comparisons
    comparison_count += 1
    overall_min = lmin if lmin < rmin else rmin
    comparison_count += 1
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


def min_max_naive(arr):
    mn, mx = arr[0], arr[0]
    comps = 0
    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x
        comps += 1
        if x > mx:
            mx = x
    return mn, mx, comps


# -------------------------------------------------------------------
# Execution Logic
# -------------------------------------------------------------------
def generate_random_input():
    # Generates a random array with a random length between 5 and 15 elements
    size = random.randint(5, 15)
    random_nums = [random.randint(0, 99) for _ in range(size)]
    entry_array.delete(0, tk.END)
    entry_array.insert(0, ", ".join(map(str, random_nums)))


def run_analysis():
    global comparison_count

    # 1. Read User Array Input
    raw_input = entry_array.get().strip()

    if not raw_input:
        messagebox.showwarning(
            "Input Error", "Please enter numbers separated by commas."
        )
        return

    try:
        # Convert comma-separated string to integer list
        sample_arr = [int(x.strip()) for x in raw_input.split(",") if x.strip() != ""]
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid integers separated by commas (e.g., 3, 1, 7, 4).",
        )
        return

    if len(sample_arr) == 0:
        messagebox.showwarning(
            "Input Error", "Array must contain at least one element."
        )
        return

    # Process Custom Array Demonstration
    comparison_count = 0
    mn, mx = min_max_dc(sample_arr, 0, len(sample_arr) - 1)
    dc_comps = comparison_count
    _, _, naive_comps = min_max_naive(sample_arr)

    # Update Demonstration UI Cards
    lbl_array_val.config(text=str(sample_arr))
    lbl_min_max_val.config(text=f"Min: {mn}  |  Max: {mx}")
    lbl_dc_val.config(text=str(dc_comps))
    lbl_naive_val.config(text=str(naive_comps))

    # 2. Dynamic Performance Scale Analysis
    # Clears old table entries
    for item in tree.get_children():
        tree.delete(item)

    base_n = len(sample_arr)
    # Dynamically scale benchmarks based on the entered array length (n, 10n, 100n, 1000n)
    sizes = [base_n, base_n * 10, base_n * 100, base_n * 1000]

    for idx, size in enumerate(sizes):
        if idx == 0:
            # First row uses your exact input array
            arr = sample_arr.copy()
        else:
            # Scaled rows generate random elements of length size
            arr = [random.randint(1, 10000) for _ in range(size)]

        comparison_count = 0
        min_max_dc(arr, 0, len(arr) - 1)
        dc = comparison_count
        _, _, naive = min_max_naive(arr)
        
        # Theoretical upper bound formula for divide & conquer min-max
        formula = 3 * size // 2 - 2

        row_tag = "even" if idx % 2 == 0 else "odd"
        tree.insert(
            "",
            "end",
            values=(
                f"{size:,}",
                f"{dc:,}",
                f"{naive:,}",
                f"{formula:,}",
            ),
            tags=(row_tag,),
        )


# -------------------------------------------------------------------
# User Interface Construction
# -------------------------------------------------------------------

# Top Header Area
header_frame = ttk.Frame(root)
header_frame.pack(fill="x", padx=20, pady=(15, 10))

title_label = ttk.Label(
    header_frame,
    text="Algorithm Analytics Dashboard",
    style="Header.TLabel",
)
title_label.pack(side="left")

subtitle_label = ttk.Label(
    header_frame,
    text="Divide & Conquer vs Naive Min-Max Analysis",
    style="Muted.TLabel",
)
subtitle_label.pack(side="left", padx=(15, 0), pady=5)

# Main Container Frame
main_container = ttk.Frame(root)
main_container.pack(fill="both", expand=True, padx=20, pady=10)

# SECTION 1: User Input & Custom Array Demonstration Card
sample_card = ttk.Frame(main_container, style="Card.TFrame")
sample_card.pack(fill="x", pady=(0, 15), ipady=10, ipadx=10)

lbl_card_title = ttk.Label(
    sample_card, text="CUSTOM ARRAY DEMONSTRATION", style="SubHeader.TLabel"
)
lbl_card_title.grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(5, 10))

# Input Row Configuration
lbl_input_prompt = ttk.Label(
    sample_card, text="Enter Array (comma-separated):", style="Muted.TLabel"
)
lbl_input_prompt.grid(row=1, column=0, sticky="w", padx=15, pady=5)

entry_array = tk.Entry(
    sample_card,
    bg="#0F172A",
    fg=TEXT_LIGHT,
    insertbackground=TEXT_LIGHT,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER_COLOR,
    font=("Consolas", 10),
)
entry_array.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
entry_array.insert(0, "3, 1, 7, 4, 9, 2, 8, 5, 6, 0")  # Default values

btn_random = ttk.Button(
    sample_card,
    text="🎲 Random",
    style="Secondary.TButton",
    command=generate_random_input,
)
btn_random.grid(row=1, column=2, padx=5, pady=5)

btn_run = ttk.Button(
    sample_card,
    text="⚡ Execute Analysis",
    style="Accent.TButton",
    command=run_analysis,
)
btn_run.grid(row=1, column=3, padx=15, pady=5)

sample_card.columnconfigure(1, weight=1)

# Parsed Array Display Box
lbl_arr_title = ttk.Label(
    sample_card, text="Active Array:", style="Muted.TLabel"
)
lbl_arr_title.grid(row=2, column=0, sticky="w", padx=15, pady=5)

lbl_array_val = ttk.Label(
    sample_card,
    text="-",
    font=("Consolas", 10, "bold"),
    foreground=ACCENT_PURPLE,
)
lbl_array_val.grid(row=2, column=1, columnspan=3, sticky="w", padx=10, pady=5)

# Sub-Metrics Container
metric_frame = ttk.Frame(sample_card, style="Card.TFrame")
metric_frame.grid(
    row=3, column=0, columnspan=4, sticky="ew", padx=15, pady=(15, 5)
)

# Metric Box 1: Calculated Min/Max
f1 = tk.Frame(metric_frame, bg="#0F172A", highlightthickness=1, highlightbackground=BORDER_COLOR)
f1.pack(side="left", expand=True, fill="both", padx=5)
tk.Label(f1, text="RESULTS", bg="#0F172A", fg=TEXT_MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
lbl_min_max_val = tk.Label(f1, text="-", bg="#0F172A", fg=TEXT_LIGHT, font=("Segoe UI", 12, "bold"))
lbl_min_max_val.pack(anchor="w", padx=10, pady=(0, 8))

# Metric Box 2: Divide & Conquer Count
f2 = tk.Frame(metric_frame, bg="#0F172A", highlightthickness=1, highlightbackground=BORDER_COLOR)
f2.pack(side="left", expand=True, fill="both", padx=5)
tk.Label(f2, text="D&C COMPARISONS", bg="#0F172A", fg=TEXT_MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
lbl_dc_val = tk.Label(f2, text="-", bg="#0F172A", fg=ACCENT_GREEN, font=("Segoe UI", 12, "bold"))
lbl_dc_val.pack(anchor="w", padx=10, pady=(0, 8))

# Metric Box 3: Naive Count
f3 = tk.Frame(metric_frame, bg="#0F172A", highlightthickness=1, highlightbackground=BORDER_COLOR)
f3.pack(side="left", expand=True, fill="both", padx=5)
tk.Label(f3, text="NAIVE COMPARISONS", bg="#0F172A", fg=TEXT_MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
lbl_naive_val = tk.Label(f3, text="-", bg="#0F172A", fg="#F43F5E", font=("Segoe UI", 12, "bold"))
lbl_naive_val.pack(anchor="w", padx=10, pady=(0, 8))

# SECTION 2: Benchmarking Table Card
table_card = ttk.Frame(main_container, style="Card.TFrame")
table_card.pack(fill="both", expand=True, ipady=10, ipadx=10)

lbl_table_title = ttk.Label(
    table_card, text="DYNAMIC PERFORMANCE ANALYSIS BY ARRAY SIZE", style="SubHeader.TLabel"
)
lbl_table_title.pack(anchor="w", padx=15, pady=(10, 5))

columns = ("size", "dc", "naive", "formula")
tree = ttk.Treeview(table_card, columns=columns, show="headings", height=6)

tree.heading("size", text="Array Size (n)", anchor="center")
tree.heading("dc", text="D&C Comparisons", anchor="center")
tree.heading("naive", text="Naive Comparisons", anchor="center")
tree.heading("formula", text="Formula (3n/2 - 2)", anchor="center")

tree.column("size", anchor="center", width=150)
tree.column("dc", anchor="center", width=180)
tree.column("naive", anchor="center", width=180)
tree.column("formula", anchor="center", width=180)

tree.tag_configure("even", background="#1E293B")
tree.tag_configure("odd", background="#111827")

tree.pack(fill="both", expand=True, padx=15, pady=10)

# Run initial calculations automatically on open
run_analysis()

# Main Application Loop
root.mainloop()
