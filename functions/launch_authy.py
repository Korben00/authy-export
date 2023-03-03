import subprocess
import platform
from functions.select_exe_file import select_exe_file

def launch_authy():
    
    # Display a message indicating that Authy is launching
    print("Launching Authy")
    
    # Determine the machine's OS
    os = platform.system()
    
    # If the OS is macOS (Darwin), launch Authy in debug mode using the 'open' command
    if os == 'Darwin':
        subprocess.run(['open', '--background', '-a', 'Authy Desktop', '--args', '--remote-debugging-port=5858'], check=True)
        subprocess.run(['osascript', '-e', 'tell application "Authy Desktop" to activate'])
        subprocess.run(['osascript', '-e', 'tell application "System Events" to keystroke "m" using command down']) 
    
    # If the OS is Linux, launch Authy in debug mode using the 'authy' command
    elif os == 'Linux':
        subprocess.run(['authy', '--no-ui', '--remote-debugging-port=5858'], check=True)
    
    # If the OS is neither macOS nor Linux, raise an exception indicating that the OS is not supported
    elif os == 'Windows':
        file = select_exe_file()
        subprocess.run([file, '--remote-debugging-port=5858'], check=True)
    else:
        raise ValueError("The OS is not supported")