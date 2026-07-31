import tkinter as tk
from tkinter import ttk, messagebox


class ModernTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task & Goal Tracker")
        self.root.geometry("850x600")
        self.root.minsize(750, 500)

        # Color Palette
        self.colors = {
            "bg": "#1e1e2e",
            "card_bg": "#252538",
            "accent": "#89b4fa",
            "accent_hover": "#b4befe",
            "text": "#cdd6f4",
            "subtext": "#a6adc8",
            "success": "#a6e3a1",
            "warning": "#f9e2af",
            "danger": "#f38ba8",
            "list_bg": "#181825",
            "select_bg": "#313244"
        }

        self.tasks = []  # List of dicts: {'title': str, 'category': str, 'priority': str, 'completed': bool}
        self.current_filter = "All"

        self.root.configure(bg=self.colors["bg"])
        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configure Progressbar
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=self.colors["card_bg"],
            background=self.colors["accent"],
            thickness=10,
            borderwidth=0
        )

    def _build_ui(self):
        # Header Frame
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=15, padx=25)
        header.pack(fill="x")

        title_lbl = tk.Label(
            header,
            text="Task Dashboard",
            font=("Segoe UI", 20, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        )
        title_lbl.pack(side="left")

        # Stats Card
        self.stats_lbl = tk.Label(
            header,
            text="0 / 0 Completed (0%)",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["accent"],
            bg=self.colors["bg"]
        )
        self.stats_lbl.pack(side="right")

        # Progress Bar
        self.progress = ttk.Progressbar(
            self.root,
            style="Custom.Horizontal.TProgressbar",
            orient="horizontal",
            mode="determinate"
        )
        self.progress.pack(fill="x", padx=25, pady=(0, 15))

        # Main Content Layout (Left: Inputs, Right: Task List)
        content = tk.Frame(self.root, bg=self.colors["bg"], padx=25)
        content.pack(fill="both", expand=True)

        # Left Column (Input Controls)
        left_panel = tk.Frame(content, bg=self.colors["card_bg"], padx=15, pady=15, width=280)
        left_panel.pack(side="left", fill="y", padx=(0, 15), pady=(0, 20))
        left_panel.pack_propagate(False)

        tk.Label(
            left_panel, text="New Task", font=("Segoe UI", 12, "bold"),
            fg=self.colors["text"], bg=self.colors["card_bg"]
        ).pack(anchor="w", pady=(0, 10))

        # Task Title Input
        tk.Label(
            left_panel, text="Task Name", font=("Segoe UI", 9),
            fg=self.colors["subtext"], bg=self.colors["card_bg"]
        ).pack(anchor="w")

        self.task_entry = tk.Entry(
            left_panel, bg=self.colors["list_bg"], fg=self.colors["text"],
            insertbackground=self.colors["text"], relief="flat", font=("Segoe UI", 10)
        )
        self.task_entry.pack(fill="x", pady=(2, 10), ipady=5)

        # Category Input
        tk.Label(
            left_panel, text="Category", font=("Segoe UI", 9),
            fg=self.colors["subtext"], bg=self.colors["card_bg"]
        ).pack(anchor="w")

        self.cat_cb = ttk.Combobox(left_panel, values=["Work", "Personal", "Study", "Health"], state="readonly")
        self.cat_cb.set("Work")
        self.cat_cb.pack(fill="x", pady=(2, 10))

        # Priority Input
        tk.Label(
            left_panel, text="Priority Level", font=("Segoe UI", 9),
            fg=self.colors["subtext"], bg=self.colors["card_bg"]
        ).pack(anchor="w")

        self.prio_cb = ttk.Combobox(left_panel, values=["Low", "Medium", "High"], state="readonly")
        self.prio_cb.set("Medium")
        self.prio_cb.pack(fill="x", pady=(2, 20))

        # Add Task Button
        add_btn = tk.Button(
            left_panel, text="+ Add Task", font=("Segoe UI", 10, "bold"),
            bg=self.colors["accent"], fg="#11111b", activebackground=self.colors["accent_hover"],
            relief="flat", cursor="hand2", command=self.add_task
        )
        add_btn.pack(fill="x", ipady=6)

        # Right Column (Task Display & Controls)
        right_panel = tk.Frame(content, bg=self.colors["bg"])
        right_panel.pack(side="right", fill="both", expand=True, pady=(0, 20))

        # Filter Tabs Frame
        filter_frame = tk.Frame(right_panel, bg=self.colors["bg"])
        filter_frame.pack(fill="x", pady=(0, 10))

        for f_name in ["All", "Pending", "Completed"]:
            btn = tk.Button(
                filter_frame, text=f_name, font=("Segoe UI", 9, "bold"),
                bg=self.colors["card_bg"], fg=self.colors["subtext"],
                activebackground=self.colors["select_bg"], activeforeground=self.colors["text"],
                relief="flat", cursor="hand2", command=lambda f=f_name: self.set_filter(f)
            )
            btn.pack(side="left", padx=(0, 5), ipadx=10, ipady=3)

        # Task Listbox Container
        list_container = tk.Frame(right_panel, bg=self.colors["card_bg"])
        list_container.pack(fill="both", expand=True)

        self.task_listbox = tk.Listbox(
            list_container, bg=self.colors["list_bg"], fg=self.colors["text"],
            selectbackground=self.colors["select_bg"], selectforeground=self.colors["text"],
            font=("Segoe UI", 10), relief="flat", highlightthickness=0, activestyle="none"
        )
        self.task_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.task_listbox.yview)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        # Action Buttons below list
        action_frame = tk.Frame(right_panel, bg=self.colors["bg"])
        action_frame.pack(fill="x", pady=(10, 0))

        complete_btn = tk.Button(
            action_frame, text="✓ Toggle Complete", font=("Segoe UI", 9, "bold"),
            bg=self.colors["success"], fg="#11111b", relief="flat", cursor="hand2", command=self.toggle_complete
        )
        complete_btn.pack(side="left", ipadx=10, ipady=4)

        delete_btn = tk.Button(
            action_frame, text="✕ Delete Task", font=("Segoe UI", 9, "bold"),
            bg=self.colors["danger"], fg="#11111b", relief="flat", cursor="hand2", command=self.delete_task
        )
        delete_btn.pack(side="right", ipadx=10, ipady=4)

    def add_task(self):
        title = self.task_entry.get().strip()
        category = self.cat_cb.get()
        priority = self.prio_cb.get()

        if not title:
            messagebox.showwarning("Validation Error", "Please enter a task name.")
            return

        self.tasks.append({
            "title": title,
            "category": category,
            "priority": priority,
            "completed": False
        })

        self.task_entry.delete(0, tk.END)
        self.render_tasks()

    def toggle_complete(self):
        selected_idx = self.get_selected_real_index()
        if selected_idx is None:
            return

        self.tasks[selected_idx]["completed"] = not self.tasks[selected_idx]["completed"]
        self.render_tasks()

    def delete_task(self):
        selected_idx = self.get_selected_real_index()
        if selected_idx is None:
            return

        del self.tasks[selected_idx]
        self.render_tasks()

    def set_filter(self, filter_name):
        self.current_filter = filter_name
        self.render_tasks()

    def get_filtered_tasks(self):
        if self.current_filter == "Pending":
            return [t for t in self.tasks if not t["completed"]]
        elif self.current_filter == "Completed":
            return [t for t in self.tasks if t["completed"]]
        return self.tasks

    def get_selected_real_index(self):
        try:
            list_idx = self.task_listbox.curselection()[0]
        except IndexError:
            messagebox.showinfo("Selection Required", "Please select a task from the list.")
            return None

        filtered = self.get_filtered_tasks()
        selected_task = filtered[list_idx]
        return self.tasks.index(selected_task)

    def render_tasks(self):
        self.task_listbox.delete(0, tk.END)
        filtered = self.get_filtered_tasks()

        for task in filtered:
            status_mark = "[✓]" if task["completed"] else "[ ]"
            display_str = f"{status_mark} [{task['priority'].upper()}] {task['title']}  •  {task['category']}"
            self.task_listbox.insert(tk.END, display_str)

            # Color styling based on status
            idx = self.task_listbox.size() - 1
            if task["completed"]:
                self.task_listbox.itemconfig(idx, fg=self.colors["subtext"])

        self._update_stats()

    def _update_stats(self):
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        pct = int((completed / total) * 100) if total > 0 else 0

        self.stats_lbl.config(text=f"{completed} / {total} Completed ({pct}%)")
        self.progress["value"] = pct


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTaskManager(root)
    root.mainloop()
