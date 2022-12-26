# Authy TOTP Extractor

This application is designed to extract TOTP (Time-based One-Time Password) information from Authy by launching Authy in debug mode and using the Chrome DevTools API to communicate with the browser. It then runs a JavaScript script to decrypt and extract the TOTP information, which can be saved to a file or displayed to the user. This can be useful for those who want to migrate their TOTP information from Authy to another service, or simply want to access and view their TOTP information in an easier way.

# Features

Extract TOTP information from Authy.

# Requirements

Authy Desktop
Python 3
PyChromeDevTools
tkinter
colorama
pyfiglet
musicalbeeps

# Installation

Clone or download this repository
Navigate to the repository directory in a terminal
Run the following command: pip install -r requirements.txt

# Usage

Run the script: python authy-export.py
The script will launch Authy in debug mode. If Authy is not already installed, it will need to be installed first.
The script will run the JavaScript script to decrypt and extract the TOTP information.
The TOTP information will be displayed to the user and can be saved to a file by entering the desired file name and pressing enter.

# Compilation

To compile the script into an executable file, run the following command:
pyinstaller --onefile --noconsole --icon ico.ico authy-export.py

# Author

Korben - https://korben.info
