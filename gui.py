import os
import tkinter as tk
from tkinter import filedialog, ttk

from main import generate_summary


def main():
    window = tk.Tk()
    window.title("Project Summary Generator")
    window.geometry("940x270")

    def pick_root_dir():
        result = filedialog.askdirectory()
        if result:
            root_dir.set(result)

    def pick_output_dir():
        result = filedialog.askdirectory()
        if result:
            output_dir.set(result)

    root_dir = tk.StringVar()
    exclude_dirs = tk.StringVar(value="venv, __pycache__, node_modules")
    include_extensions = tk.StringVar(value=".md, .html, .css, .txt, .json, .yml, .yaml, .py, .ts, .js")
    output_file = tk.StringVar(value="summary.md")
    output_dir = tk.StringVar(value=os.path.expanduser("~/Desktop"))
    target_files = tk.StringVar(value="Dockerfile")  # 初期値を設定

    ttk.Label(window, text="Root Directory:").grid(row=0, column=0, sticky=tk.W)
    ttk.Entry(window, textvariable=root_dir, width=50, state="readonly").grid(row=0, column=1)
    ttk.Button(window, text="Browse", command=pick_root_dir).grid(row=0, column=2)

    ttk.Label(window, text="Exclude Directories (comma-separated):").grid(row=1, column=0, sticky=tk.W)
    ttk.Entry(window, textvariable=exclude_dirs, width=50).grid(row=1, column=1)

    ttk.Label(window, text="Include Extensions (comma-separated):").grid(row=2, column=0, sticky=tk.W)
    ttk.Entry(window, textvariable=include_extensions, width=50).grid(row=2, column=1)

    ttk.Label(window, text="Output File Name:").grid(row=3, column=0, sticky=tk.W)
    ttk.Entry(window, textvariable=output_file, width=50).grid(row=3, column=1)

    ttk.Label(window, text="Output Directory:").grid(row=4, column=0, sticky=tk.W)
    ttk.Entry(window, textvariable=output_dir, width=50, state="readonly").grid(row=4, column=1)
    ttk.Button(window, text="Browse", command=pick_output_dir).grid(row=4, column=2)

    ttk.Label(window, text="Target Files (comma-separated):").grid(row=5, column=0, sticky=tk.W)
    ttk.Entry(window, textvariable=target_files, width=50).grid(row=5, column=1)

    def generate_summary_callback():
        generate_summary(
            root_dir.get(),
            exclude_dirs.get().split(","),
            include_extensions.get().split(","),
            output_file.get(),
            output_dir.get(),
            target_files.get().split(",")
        )

    ttk.Button(window, text="Generate Summary", command=generate_summary_callback).grid(row=6, column=1, pady=10)

    window.mainloop()


if __name__ == "__main__":
    main()