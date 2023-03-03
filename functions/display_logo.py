import pyfiglet
import tkinter as tk

def display_logo():
    logo = pyfiglet.figlet_format("AUTHY", font="slant")
    label = tk.Label(text=logo, font=("Courier", 15), fg="white", bg="black", padx=10, pady=10)
    label.pack()

def display_logo_korben():
    logo = pyfiglet.figlet_format("TOTP Extractor", font="sblood")
    label = tk.Label(text=logo, font=("Courier", 7), fg="red", bg="black")
    label.pack()