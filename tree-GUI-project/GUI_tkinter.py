import tkinter as tk
from tkinter import messagebox
import csv
import os


class TreeGUI(tk.Tk):
    CSV_FILE = "Street_Tree_List_20250908.csv"

    def __init__(self):
        super().__init__()

        self.title("🌳 Tree Search System")
        self.geometry("520x220")
        self.resizable(False, False)

        # --- Frames ---
        self.top_frame = tk.Frame(self, pady=10)
        self.bottom_frame = tk.Frame(self, padx=10, pady=10)

        # --- Input Section ---
        tk.Label(
            self.top_frame,
            text="Enter Tree ID:",
            font=("Arial", 11)
        ).pack(side="left")

        self.id_entry = tk.Entry(self.top_frame, font=("Arial", 11), width=12)
        self.id_entry.pack(side="left", padx=(5, 10))

        tk.Button(
            self.top_frame,
            text="Search",
            command=self.search_tree,
            width=10,
            font=("Arial", 11)
        ).pack(side="left", padx=5)

        tk.Button(
            self.top_frame,
            text="Quit",
            command=self.destroy,
            font=("Arial", 11)
        ).pack(side="left")

        # --- Output Section ---
        self.tree_info = tk.StringVar()
        self.info_label = tk.Label(
            self.bottom_frame,
            textvariable=self.tree_info,
            anchor="nw",
            justify="left",
            font=("Arial", 11),
            width=60
        )
        self.info_label.pack()

        # Pack frames
        self.top_frame.pack()
        self.bottom_frame.pack()

    # -------------------------
    # Main search logic
    # -------------------------
    def search_tree(self):
        tree_id = self.id_entry.get().strip()

        if not tree_id:
            messagebox.showinfo("Input Needed", "Please enter a tree ID.")
            return

        if not os.path.exists(self.CSV_FILE):
            messagebox.showerror("Error", f"CSV file not found:\n{self.CSV_FILE}")
            return

        found = False

        # Open and read CSV
        with open(self.CSV_FILE, encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)  # skip header if exists

            for row in reader:
                if row[0] == tree_id:
                    self.tree_info.set(
                        f"Tree ID:  {row[0]}\n"
                        f"Status:   {row[1]}\n"
                        f"Species:  {row[2]}\n"
                        f"Address:  {row[3]}"
                    )
                    found = True
                    break

        if not found:
            messagebox.showwarning("Not Found", f"No tree with ID {tree_id} found.")
            self.tree_info.set("")

        self.id_entry.delete(0, tk.END)


if __name__ == "__main__":
    app = TreeGUI()
    app.mainloop()
