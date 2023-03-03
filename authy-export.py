#!/usr/bin/env python3
"""
Authy TOTP Extractor

This application is designed to extract TOTP (Time-based One-Time Password) information from Authy. 
It does this by launching Authy in debug mode and using the Chrome DevTools API to communicate 
with the browser. The application then runs a JavaScript script to decrypt and extract the TOTP 
information, which it can then save to a file or display to the user. This can be useful for 
those who want to migrate their TOTP information from Authy to another service, or simply want to 
access and view their TOTP information in an easier way.

Author: Korben
Version: 1.0
Website: https://korben.info
Date: 25/12/2022
"""
# To compile : pyinstaller --onefile --noconsole --icon ico.ico authy-export.py
import tkinter as tk
import PyChromeDevTools
import platform
import subprocess
import time
import webbrowser
import colorama
import threading


from functions.display_logo import display_logo, display_logo_korben
from functions.select_exe_file import select_exe_file
from functions.launch_authy import launch_authy
from functions.export import export
from functions.music import play_sound
from functions.checktokenslist import check_tokens_list

# Define the function to quit Authy and close the program
def quit_authy():
    
    # Display a message indicating that Authy is quitting
    os = platform.system()
    
    # Stop Authy
    if os == 'Darwin':
        subprocess.run(['killall', 'Authy Desktop'], check=True)
    elif os == 'Linux':
        subprocess.run(['pkill', 'authy'], check=True)
    else:
        raise ValueError("The OS is not supported.")
    root.destroy()
    tk.Tk().quit()
    
# Define the function to execute when the button is clicked
def on_button_click():
    
    # Disable the button
    button.configure(state='disabled', text='Please wait...')
    root.update()
    
    # Start Authy
    launch_authy()
    
    # Wait for the tokens list to be loaded
    time.sleep(3)
    
    # Export the TOTP
    chromex = PyChromeDevTools.ChromeInterface(host='localhost', port=5858)
    chromex.Network.enable()
    
    # Wait for the tokens list to be loaded
    tokens_list = None
    while tokens_list is None:
        tokens_list = check_tokens_list(chromex)
        time.sleep(0.1)
    
    # Export the TOTP
    chromex.close()
    
    # Stop Authy
    export()
    button.configure(state='normal', text='Quit', command=quit_authy)
    label['text'] = ' TOTP data extracted successfully! You\'re amazing! '
    label["font"] = 'Helvetica 20 bold'

# Define the function to rotate the text in the label
def rotate_text():
    current_text = label["text"]
    new_text = current_text[1:] + current_text[0]
    label.config(text=new_text)
    root.after(100, rotate_text)


# Initialize the root window
colorama.init()

# Create the root window
root = tk.Tk()

# background color black
bg_color = '#000000'

# foreground color white
fg_color = '#ffffff'
root.configure(background=bg_color)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate x and y coordinates for the center of the screen
x = (screen_width / 2) - (500 / 2)  # 500 is the width of the window
y = (screen_height / 2) - (400 / 2)  # 400 is the height of the window

# Set window size and position
root.geometry('500x400+{}+{}'.format(int(x), int(y)))
root.title("Authy TOTP Extractor - Korben")
root.resizable(False, False)

# Set the font for the label and button
font = ('Helvetica', 16)

# Set the hover color for the button
hover_color = '#cccccc'
display_logo()
display_logo_korben()

# Create the button
button = tk.Button(root, text="Click to export TOTP", font=font, bg=bg_color, activebackground='#999999', activeforeground='#ffffff', command=on_button_click, width=15, height=2, padx=10, pady=10)
button.pack()

# Add hover effect to the button
button.bind("<Enter>", lambda event: event.widget.configure(bg=hover_color))
button.bind("<Leave>", lambda event: event.widget.configure(bg=bg_color))

# Create the label with the text to scroll, label with a width of 200 pixels.
label = tk.Label(root, text=" KORBEN.INFO ", font=('Helvetica', 13, 'underline'), bg=bg_color, fg=fg_color, pady=100, width=400)

# Make this label clickable to open url https://korben.info
label.bind("<Button-1>", lambda e: webbrowser.open_new("https://korben.info"))
label.pack()

# Update every 100 ms
root.after(1, rotate_text)

# Create a new thread for musicalbeeps
thread = threading.Thread(target=play_sound)

# start the thread until the program is closed
thread.daemon = True
thread.start()
root.mainloop()
