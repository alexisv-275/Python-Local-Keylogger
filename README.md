# Educational Keylogger

A Python-based keylogger developed for educational purposes to understand keyboard event capture and user-system interaction analysis.

## ⚠️ Disclaimer

**This tool is for EDUCATIONAL PURPOSES ONLY.** It is designed to be used on your own computer to learn about:
- Keyboard event monitoring
- System interaction logging
- Security awareness and detection methods

**Never use this tool without explicit permission on devices you don't own.** Unauthorized use of keyloggers is illegal in most jurisdictions.

## 🎯 Features
<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/d2f83eb0-fb89-4bab-9c5a-fe7c74cb367d" alt="Feature 1" width="480" />
      <br />
      <sub><b>Script executed</b></sub>
    </td>
     <td align="center">
      <img src="https://github.com/user-attachments/assets/987a1015-f4fc-4279-ad8b-5bd2373b29fb" alt="Feature 2" width="480" />
      <br />
      <sub><b>CSV example</b></sub>
    </td>
  </tr>
</table>

- **Word-by-word capture**: Accumulates characters into complete words for better readability
- **Timestamp logging**: Records date and time for each keystroke/word
- **Active application tracking**: Identifies which program the user is typing in (Windows only)
- **CSV format**: Structured data storage for easy analysis in Excel or other tools
- **Special key handling**: Logs special keys like Enter, Space, Backspace, Tab, etc.
- **Background operation**: Runs invisibly without disrupting user activities
- **Low resource consumption**: Minimal CPU and memory usage
- **Persistent logging**: Appends to existing logs without overwriting previous data

## 📋 Requirements

- Python 3.7 or higher
- Windows OS (for active window capture feature)
- Required Python packages (see Installation)

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/educational-keylogger.git
   cd educational-keylogger
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install pynput pywin32 psutil
   ```

## 🚀 Usage

### Basic Usage

Run the keylogger manually:

```bash
python Keylogger.py
```

- The keylogger will start capturing keystrokes
- Press **ESC** to stop the keylogger
- Logs are saved to `key_log.csv` in the same directory

### CSV Output Format

The output file `key_log.csv` contains the following columns:

| Date       | Time     | Key/Word | Application              |
|------------|----------|----------|--------------------------|
| 2025-11-02 | 14:30:15 | hello    | chrome.exe - Google Chrome |
| 2025-11-02 | 14:30:16 | [SPACE]  | chrome.exe - Google Chrome |
| 2025-11-02 | 14:30:18 | world    | chrome.exe - Google Chrome |

### Auto-start on Windows Login (Optional)

To automatically run the keylogger when Windows starts:

1. **Create a startup script** (`run_keylogger.bat`):
   ```batch
   @echo off
   cd /d "C:\PATH\TO\YOUR\KEYLOGGER\FOLDER"
   start /B pythonw.exe "Keylogger.py"
   ```
   **⚠️ IMPORTANT**: Replace `C:\PATH\TO\YOUR\KEYLOGGER\FOLDER` with the actual path to your keylogger folder.

2. **Add to Windows Registry**:
   ```powershell
   $keyPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
   $scriptPath = "C:\PATH\TO\YOUR\run_keylogger.bat"
   New-ItemProperty -Path $keyPath -Name "EducationalKeylogger" -Value $scriptPath -PropertyType String -Force
   ```
   **⚠️ IMPORTANT**: Replace `C:\PATH\TO\YOUR\run_keylogger.bat` with the actual path to your batch file.

3. **To remove auto-start**:
   ```powershell
   Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "EducationalKeylogger"
   ```

### Manual Process Management

**Check if keylogger is running**:
```powershell
Get-Process python
```

**Stop all Python processes** (use with caution):
```powershell
Stop-Process -Name "python" -Force
```

## 🛡️ Antivirus Detection

**Expected behavior**: Antivirus software will likely flag this program as a threat because it exhibits typical keylogger behavior (keyboard monitoring, file writing, background execution).

**This is NORMAL** - the program is designed to behave like a keylogger for educational purposes.

### To allow execution:

1. **Add an exception** in your antivirus software for:
   - The keylogger folder
   - `Keylogger.py`
   - `run_keylogger.bat` (if using auto-start)

2. **Example for Windows Defender**:
   - Open Windows Security
   - Go to Virus & threat protection → Manage settings
   - Scroll to Exclusions → Add an exclusion
   - Choose "Folder" and select your keylogger directory

## 📊 Technical Details

### How It Works

1. **Event Listener**: Uses `pynput` library to listen for keyboard events
2. **Buffer System**: Accumulates characters until a word separator (space/enter) is detected
3. **CSV Writing**: Appends each word/key with timestamp to the CSV file
4. **Window Tracking**: Uses `win32gui` and `psutil` to identify the active application

