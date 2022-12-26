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
# Pour compiler : pyinstaller --onefile --noconsole --icon ico.ico authy-export.py

import tkinter as tk
import PyChromeDevTools
import platform
import subprocess
import time
import musicalbeeps
import threading
import webbrowser
import colorama
import pyfiglet


def display_logo():
    logo = pyfiglet.figlet_format("AUTHY", font="slant")
    label = tk.Label(text=logo, font=("Courier", 15), fg="white", bg="black", padx=10, pady=10)
    label.pack()


def display_logo_korben():
    logo = pyfiglet.figlet_format("TOTP Extractor", font="sblood")
    label = tk.Label(text=logo, font=("Courier", 7), fg="red", bg="black")
    label.pack()

def launch_authy():
    # Display a message indicating that Authy is launching
    print("Launching Authy")
    # Determine the machine's OS
    os = platform.system()
    # If the OS is macOS (Darwin), launch Authy in debug mode using the 'open' command
    if os == 'Darwin':
        subprocess.run(['open', '-a', 'Authy Desktop', '--args', '--remote-debugging-port=5858'], check=True)
    # If the OS is Linux, launch Authy in debug mode using the 'authy' command
    elif os == 'Linux':
        subprocess.run(['authy', '--remote-debugging-port=5858'], check=True)
    # If the OS is neither macOS nor Linux, raise an exception indicating that the OS is not supported
    else:
        raise ValueError("The OS is not supported")




def export():
    # Create a ChromeInterface object to communicate with the Chrome DevTools API
    chrome = PyChromeDevTools.ChromeInterface(host='localhost', port=5858)
    # Enable the Network and Page domains to allow access to their features
    chrome.Network.enable()
    chrome.Page.enable()
    # Define a JavaScript script to be run in the browser
    # Source : https://kinduff.com/2021/10/24/migrate-authy-to-bitwarden/
    script="""function hex_to_b32(hex) {
    let alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567", bytes = [];
    for (let i = 0; i < hex.length; i += 2) {
        bytes.push(parseInt(hex.substr(i, 2), 16));
    }
    let bits = 0, value = 0, output = "";
    for (let i = 0; i < bytes.length; i++) {
        value = (value << 8) | bytes[i];
        bits += 8;
        while (bits >= 5) {
        output += alphabet[(value >>> (bits - 5)) & 31];
        bits -= 5;
        }
    }
    if (bits > 0) output += alphabet[(value << (5 - bits)) & 31];
    return output;
    }
    function uuidv4() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == "x" ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
    }
    function saveToFile(content, mimeType, filename) {
    if (!content) {
        console.error("Console.save: No content");
        return;
    }
    if (typeof content === "object") content = JSON.stringify(content, undefined, 2);
    const a = document.createElement("a")
    const blob = new Blob([content], { type: mimeType })
    const url = URL.createObjectURL(blob)
    a.setAttribute("href", url)
    a.setAttribute("download", filename)
    a.click()
    }
    function deEncrypt({ log = false, save = false }) {
    const folder = { id: uuidv4(), name: "Imported from Authy by Authy TOTP Extractor @Korben" };
    const bw = {
        "encrypted": false,
        "folders": [
        folder
        ],
        "items": appManager.getModel().map((i) => {
        const secret = (i.markedForDeletion === false ? i.decryptedSeed : hex_to_b32(i.secretSeed));
        const period = (i.digits === 7 ? 10 : 30);

        const [issuer, rawName] = (i.name.includes(":"))
            ? i.name.split(":")
            : ["", i.name];
        const name = [issuer, rawName].filter(Boolean).join(": ");
        const totp = `otpauth://totp/${rawName.trim()}?secret=${secret}&digits=${i.digits}&period=${period}${issuer ? "&issuer=" + issuer : ""}`;
        return ({
            id: uuidv4(),
            organizationId: null,
            folderId: folder.id,
            type: 1,
            reprompt: 0,
            name,
            notes: null,
            favorite: false,
            login: {
            username: null,
            password: null,
            totp
            },
            collectionIds: null
        });
        }),
    };
    if (log) console.log(JSON.stringify(bw));
    if (save) saveToFile(bw, "text/json", "authy-export.json");
    }
    deEncrypt({ log: true, save: true });"""
    # Run the script in the browser
    chrome.Runtime.evaluate(expression=script)
    # Wait for the script to finish running
    chrome.close()

def quit_authy():
    # Display a message indicating that Authy is quitting
    os = platform.system()
    # Stop Authy
    if os == 'Darwin':
        subprocess.run(['killall', 'Authy Desktop'], check=True)
    elif os == 'Linux':
        subprocess.run(['pkill', 'authy'], check=True)
    else:
        raise ValueError("The OS is not supporte")
    root.destroy()
    tk.Tk().quit()
    # Exit the program


def check_tokens_list(chromex):
    # Check if the tokens list is loaded
    result = chromex.Runtime.evaluate(expression="document.getElementById('tokens-list').innerHTML")
    try : 
        result = result[1][0]['result']['result']['value']
    except:
        print('C BAD')
        return False
    else:
        return True

def on_button_click():
    # Disable the button
    button['state'] = 'disabled'
    # Start Authy
    launch_authy()
    # Wait for the tokens list to be loaded
    time.sleep(3)
    # Export the TOTP
    chromex = PyChromeDevTools.ChromeInterface(host='localhost', port=5858)
    chromex.Network.enable()
    # Wait for the tokens list to be loaded
    while check_tokens_list(chromex) == False:
        time.sleep(0.1)
    # Export the TOTP
    chromex.close()
    # Stop Authy
    export()
    #replace the button text by "Quit"
    button['text'] = 'Quit'
    #Activate the button
    button['state'] = 'normal'
    # Bind the button to the quit function
    button['command'] = quit_authy
    #button.destroy()
    # Create the quit button
    #quit_button = tk.Button(root, text="Quit", font=font, bg=bg_color, fg=fg_color, command=quit_authy, width=150, height=10)
    #quit_button.pack()
    # replace the label text
    label['text'] = ' TOTP data extracted successfully! You\'re amazing! '
    label["font"] = 'Helvetica 20 bold'

# Function that updates the content of the label
def update_label():
    current_text = label["text"]
    new_text = current_text[1:] + current_text[0]
    label.config(text=new_text)
    root.after(100, update_label)

# use musicalbeeps to play a sound without blocking the GUI
def play_sound():
    player = musicalbeeps.Player(volume = 0.1,
                            mute_output = True)
    # play the notes of the melody
    note_duration = 0.15
    player.play_note("D", note_duration)
    melody = ["C", "D", "E", "F", "G", "A", "B", "C"]
    while True:
        # First verse
        for i in range(4):
            player.play_note("G", note_duration * 2)
            player.play_note("F", note_duration)
            player.play_note("E", note_duration)
            player.play_note("D", note_duration * 2)

        # Chorus
        for i in range(2):
            player.play_note("C", note_duration * 2)
            player.play_note("G", note_duration)
            player.play_note("F", note_duration)
            player.play_note("C", note_duration * 2)
            player.play_note("G", note_duration)
            player.play_note("F", note_duration)
            player.play_note("E", note_duration * 2)
            player.play_note("C", note_duration)
            player.play_note("D", note_duration)
            player.play_note("E", note_duration * 2)

        # Second verse
        for i in range(4):
            player.play_note("F", note_duration)
            player.play_note("G", note_duration)
            player.play_note("A", note_duration)
            player.play_note("G", note_duration)
            player.play_note("F", note_duration)
            player.play_note("E", note_duration)
            player.play_note("D", note_duration)
            player.play_note("C", note_duration)
            player.play_note("B", note_duration)
            player.play_note("A", note_duration)

        # Bridge
        for i in range(2):
            player.play_note("G", note_duration * 2)
            player.play_note("D", note_duration)
            player.play_note("C", note_duration * 2)
            player.play_note("G", note_duration)
            player.play_note("B", note_duration)
            player.play_note("A", note_duration * 2)
            player.play_note("G", note_duration)
            player.play_note("F", note_duration)
            player.play_note("E", note_duration * 2)

        # Chorus
        for i in range(2):
            player.play_note("C", note_duration * 2)
            player.play_note("G", note_duration)
            player.play_note("F", note_duration)
            player.play_note("C", note_duration * 2)
            player.play_note("G", note_duration)
            player.play_note("F", note_duration)
            player.play_note("E", note_duration * 2)
            player.play_note("C", note_duration)
            player.play_note("D", note_duration)
            player.play_note("E", note_duration * 2)


colorama.init()
# Create the root window
root = tk.Tk()
root.title("Authy TOTP Extractor")
# background color black
bg_color = '#000000'
# foreground color white
fg_color = '#ffffff'
root.configure(background=bg_color)
root.geometry("500x400")
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
# Create the label with the text to scroll, label width 200 pixels
label = tk.Label(root, text=" KORBEN.INFO ", font=('Helvetica', 13, 'underline'), bg=bg_color, fg=fg_color, pady=100, width=400)
#make this label clickable to open url https://korben.info
label.bind("<Button-1>", lambda e: webbrowser.open_new("https://korben.info"))
label.pack()


# Update the label content every 100 ms
root.after(1, update_label)



# Create a new thread
thread = threading.Thread(target=play_sound)
# start the thread until the program is closed
thread.daemon = True
thread.start()


root.mainloop()
