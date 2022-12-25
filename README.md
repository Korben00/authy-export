#Authy TOTP Extractor

Authy TOTP Extractor is a Python application that allows you to extract Time-based One-Time Password (TOTP) information from Authy. It does this by launching Authy in debug mode and using the Chrome DevTools API to communicate with the browser. The application then runs a JavaScript script to decrypt and extract the TOTP information, which it can then save to a file or display to the user.

#Prerequisites

Python 3
Authy
PyChromeDevTools
musicalbeeps
colorama
pyfiglet

#How to use

Make sure you have all the prerequisites installed.
Clone or download this repository.
Navigate to the directory where you cloned or downloaded the repository.
Run the following command to launch the application: python authy-export.py
The application will launch and prompt you to enter a path to save the TOTP information.
Enter the path and press Enter.
The application will then launch Authy in debug mode and extract the TOTP information.
When the process is complete, a message will be displayed indicating that the TOTP information has been saved to the specified file.

#Note

The application currently only supports macOS and Linux. It may work on other platforms, but this has not been tested.

Compiling

To compile the application into a standalone executable, you can use the following command: `pyinstaller --onefile --n
