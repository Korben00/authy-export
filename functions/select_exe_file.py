import tkinter as tk
from tkinter import filedialog

def select_exe_file():
    root = tk.Tk()
    root.withdraw()
    top = tk.Toplevel(root)
    top.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("EXE files", "*.exe")])
    root.destroy()
    return file_path