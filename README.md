# Authy Export - TOTP Extractor

<p align="center">
  <img src="https://korben.info/app/uploads/2023/03/SCR-20230303-o0u-2.webp">
</p>

This application is designed to extract TOTP (Time-based One-Time Password) information from Authy by launching Authy in debug mode and using the Chrome DevTools API to communicate with the browser. It then runs a JavaScript script to decrypt and extract the TOTP information, which can be saved to a file or displayed to the user. This can be useful for those who want to migrate their TOTP information from Authy to another service, or simply want to access and view their TOTP information in an easier way.

# Features

Extract TOTP information from Authy macOS / Linux.

# Requirements

* Authy Desktop <= 2.2.3
* Python 3
* PyChromeDevTools
* tkinter
* pyfiglet
* musicalbeeps
* colorama
* qrcode

# Installation

Install Authy desktop (<= version 2.2.3).

* macOS: https://pkg.authy.com/authy/stable/2.2.3/darwin/x64/Authy%20Desktop-2.2.3.dmg
* Win64: https://pkg.authy.com/authy/stable/2.2.3/win32/x64/Authy%20Desktop%20Setup%202.2.3.exe
* Win32: https://pkg.authy.com/authy/stable/2.2.3/win32/x32/Authy%20Desktop%20Setup%202.2.3.exe

(thanks to @gboudreau for the links)

In case your Authy Desktop updates itself without any notification, just close it, reinstall version 2.2.3, and then reopen it.

On Windows, you may have to delete the update file found in the Authy Desktop's file location (inside the app-2.2.3 folder) after starting up version 2.2.3 to stop automatic updates.

For Mac users, you can enter the given command in Terminal prior to launching Authy Desktop, which will prevent automatic updates:

mkdir -p ~/Library/Caches/com.authy.authy-mac.ShipIt ; rm -rf ~/Library/Caches/com.authy.authy-mac.ShipIt/* ; chmod 500 ~/Library/Caches/com.authy.authy-mac.ShipIt

Clone or download this repository
Navigate to the repository directory in a terminal
Run the following command: 

* pip install -r requirements.txt

Linux: You need python3-dev libasound2-dev to install musicalbeeps package.

# Usage

Run the script: python authy-export.py
The script will launch Authy in debug mode. If Authy is not already installed, it will need to be installed first.
The script will run the JavaScript script to decrypt and extract the TOTP information.
The TOTP information will be displayed to the user and can be saved to a file by entering the desired file name and pressing enter.

# Execution

git clone https://github.com/Korben00/authy-export.git

cd AuthyExtractor

python3 authy-export.py

# Compilation

To compile the script into an executable file, run the following command:

* pyinstaller --collect-all pyfiglet --onefile --noconsole --icon ico.ico authy-export.py

# Author

Korben - https://korben.info
