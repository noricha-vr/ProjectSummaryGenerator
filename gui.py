# gui.py

import tkinter.messagebox as messagebox
import os
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk

from config import (
    EXCLUDE_DIRS, DEFAULT_OUTPUT_FILENAME, DEFAULT_TARGET_FILES,
    SUPPORTED_EXTENSIONS, DEFAULT_OUTPUT_DIR
)
from main import generate_summary

def main():
    window = tk.Tk()
    window.title("Project Summary Generator")
    window.geometry("820x450")  # ウィンドウサイズを少し大きくしました

    def pick_root_dir():
        result = filedialog.askdirectory()
        if result:
            root_dir.set(result)

    def pick_output_dir():
        result = filedialog.askdirectory()
        if result:
            output_dir.set(result)

    root_dir = tk.StringVar()
    exclude_dirs = tk.StringVar(value=", ".join(EXCLUDE_DIRS))
    output_file = tk.StringVar(value=DEFAULT_OUTPUT_FILENAME)
    output_dir = tk.StringVar(value=DEFAULT_OUTPUT_DIR)
    target_files = tk.StringVar(value=", ".join(DEFAULT_TARGET_FILES))

    extension_vars = {ext: tk.BooleanVar(value=False) for ext in SUPPORTED_EXTENSIONS}

    ttk.Label(window, text="ルートディレクトリ:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
    ttk.Entry(window, textvariable=root_dir, width=50, state="readonly").grid(row=0, column=1, padx=10, pady=5)
    ttk.Button(window, text="参照", command=pick_root_dir).grid(row=0, column=2, padx=10, pady=5)

    ttk.Label(window, text="除外ディレクトリ (カンマ区切り):").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
    ttk.Entry(window, textvariable=exclude_dirs, width=50).grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(window, text="含める拡張子:").grid(row=2, column=0, sticky=tk.NW, padx=10, pady=5)
    extension_frame = ttk.Frame(window)
    extension_frame.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
    for i, ext in enumerate(SUPPORTED_EXTENSIONS):
        ttk.Checkbutton(extension_frame, text=ext, variable=extension_vars[ext]).grid(row=i//5, column=i%5, sticky=tk.W, padx=5, pady=2)

    ttk.Label(window, text="出力ファイル名:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    ttk.Entry(window, textvariable=output_file, width=50).grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(window, text="出力ディレクトリ:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
    ttk.Entry(window, textvariable=output_dir, width=50, state="readonly").grid(row=4, column=1, padx=10, pady=5)
    ttk.Button(window, text="参照", command=pick_output_dir).grid(row=4, column=2, padx=10, pady=5)

    ttk.Label(window, text="対象ファイル (カンマ区切り):").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
    ttk.Entry(window, textvariable=target_files, width=50).grid(row=5, column=1, padx=10, pady=5)

    def open_output_directory(path):
        if os.path.exists(path):
            if os.name == 'nt':  # Windows
                os.startfile(path)
            elif os.name == 'posix':  # macOS and Linux
                subprocess.call(('open', path))
        else:
            messagebox.showerror("エラー", f"ディレクトリが見つかりません：\n{path}")

    def generate_summary_callback():
        selected_extensions = [ext for ext, var in extension_vars.items() if var.get()]
        output_path = os.path.join(output_dir.get(), output_file.get())

        try:
            generate_summary(
                root_dir.get(),
                [dir.strip() for dir in exclude_dirs.get().split(",")],
                selected_extensions,
                output_file.get(),
                output_dir.get(),
                [file.strip() for file in target_files.get().split(",")]
            )

            result = messagebox.askquestion("成功",
                                            f"サマリーが正常に生成されました。\n\n出力先: {output_path}\n\n出力ディレクトリを開きますか？",
                                            icon='info')
            if result == 'yes':
                open_output_directory(output_dir.get())
        except Exception as e:
            messagebox.showerror("エラー", f"サマリーの生成中にエラーが発生しました：\n{str(e)}")

    ttk.Button(window, text="サマリーを生成", command=generate_summary_callback).grid(row=6, column=1, pady=20)

    window.mainloop()

if __name__ == "__main__":
    main()