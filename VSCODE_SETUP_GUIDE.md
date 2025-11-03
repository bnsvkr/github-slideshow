# VS Code Setup Guide - NSE Options Algo Trading System

## Complete Setup Instructions Using Visual Studio Code

This guide provides step-by-step instructions for setting up the algorithmic trading system using VS Code.

---

## 📥 Step 1: Install VS Code

If you haven't already:

1. Download VS Code from https://code.visualstudio.com/
2. Install VS Code on your system
3. Launch VS Code

---

## 🔌 Step 2: Install Required VS Code Extensions

Open VS Code and install these recommended extensions:

### Essential Extensions:

1. **Python** (by Microsoft)
   - Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac) to open Extensions
   - Search for "Python"
   - Click "Install" on the Microsoft Python extension

2. **Pylance** (by Microsoft)
   - Should install automatically with Python extension
   - Provides IntelliSense and type checking

### Recommended Extensions:

3. **Git Graph**
   - Visualize your Git branches and commits
   - Search "Git Graph" and install

4. **JSON** (by ZainChen)
   - Better JSON editing for config files
   - Search "JSON" and install

---

## 📥 Step 3: Download/Clone the Project in VS Code

### Option A: Clone Using VS Code (Recommended)

1. **Open Command Palette**:
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)

2. **Clone Repository**:
   - Type "Git: Clone"
   - Press Enter
   - Paste repository URL: `https://github.com/bnsvkr/github-slideshow.git`
   - Choose a folder location (e.g., `C:\Trading` or `~/Trading`)
   - Click "Select Repository Location"

3. **Open the Cloned Repository**:
   - VS Code will ask "Would you like to open the cloned repository?"
   - Click "Open"

4. **Switch to Trading Branch**:
   - Click on the branch name in the bottom-left corner (shows "main" or "master")
   - Select `copilot/create-algo-trading-setup` from the list
   - Or use Terminal: `git checkout copilot/create-algo-trading-setup`

### Option B: Download ZIP and Open in VS Code

1. **Download ZIP**:
   - Go to https://github.com/bnsvkr/github-slideshow
   - Click green "Code" button → "Download ZIP"
   - Extract to a folder (e.g., `C:\Trading\github-slideshow`)

2. **Open in VS Code**:
   - In VS Code: `File` → `Open Folder...`
   - Navigate to the extracted folder
   - Click "Select Folder"

---

## 🐍 Step 4: Set Up Python in VS Code

### 4.1 Install Python

If Python isn't installed:

**Windows**:
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"

**Mac**:
```bash
brew install python3
```

**Linux**:
```bash
sudo apt install python3 python3-pip  # Ubuntu/Debian
```

### 4.2 Select Python Interpreter in VS Code

1. **Open Command Palette**: `Ctrl+Shift+P` (or `Cmd+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose the Python version (3.8 or higher)
   - Example: `Python 3.10.0 64-bit` or `Python 3.11.0`

You should see the selected Python version in the bottom-left corner of VS Code.

---

## 📦 Step 5: Install Dependencies Using VS Code Terminal

### 5.1 Open Integrated Terminal

- Press `` Ctrl+` `` (backtick) or `Ctrl+Shift+` `
- Or: `View` → `Terminal`

The terminal will open at the bottom of VS Code, already in your project directory.

### 5.2 Install Required Packages

In the VS Code terminal, run:

```bash
pip install -r requirements.txt
```

Or if the above doesn't work:
```bash
python -m pip install -r requirements.txt
```

You should see the packages being installed:
- numpy
- pandas
- scipy
- requests

---

## 🔑 Step 6: Configure Fyers API Credentials

### 6.1 Get Fyers Credentials

1. **Create Fyers Account**: https://fyers.in
2. **Create API App**: https://myapi.fyers.in/
   - Go to "My Apps"
   - Click "Create New App"
   - App Name: `AlgoTrading`
   - Redirect URL: `https://127.0.0.1`
   - Note your **App ID** (Client ID)
3. **Generate Access Token**:
   - Go to https://myapi.fyers.in/generate-access-token
   - Select your app
   - Generate and copy the token

### 6.2 Create Configuration File in VS Code

1. **Open `config.example.json`**:
   - In VS Code Explorer (left sidebar), find and click `config.example.json`

2. **Create Your Config**:
   - Right-click on `config.example.json`
   - Select "Copy"
   - Right-click in the Explorer
   - Select "Paste"
   - Rename the copy to `config.json`

   Or use the terminal:
   ```bash
   cp config.example.json config.json
   ```

3. **Edit `config.json`**:
   - Click on `config.json` in the Explorer
   - Update with your credentials:

```json
{
  "fyers": {
    "client_id": "YOUR_APP_ID_HERE",
    "access_token": "YOUR_ACCESS_TOKEN_HERE",
    "redirect_uri": "https://127.0.0.1"
  },
  "trading": {
    "symbols": [
      "NSE:NIFTY50-INDEX",
      "NSE:BANKNIFTY-INDEX",
      "NSE:SBIN-EQ"
    ],
    "risk_tolerance": "moderate",
    "initial_stop_loss_pct": 2.0,
    "initial_target_pct": 5.0,
    "trailing_stop_pct": 1.5
  },
  "schedule": {
    "enabled": false,
    "start_time": "09:20",
    "end_time": "15:20",
    "check_interval_minutes": 5
  },
  "logging": {
    "level": "INFO",
    "log_file": "trading.log",
    "console_output": true
  }
}
```

4. **Save**: Press `Ctrl+S` (or `Cmd+S` on Mac)

---

## ✅ Step 7: Run Tests in VS Code

### Option A: Using Terminal

In the VS Code integrated terminal:

```bash
python test_system.py
```

You should see:
```
============================================================
NSE Options Trading System - Component Tests
============================================================

Testing Technical Indicators...
  ✓ RSI calculated: XX.XX
  ✓ MACD calculated: X.XX
✅ Technical Indicators: PASSED

...

Test Results: 5 passed, 0 failed
============================================================
```

### Option B: Using VS Code Run Button

1. Open `test_system.py` in VS Code
2. You'll see a ▶️ "Run Python File" button in the top-right corner
3. Click it to run the tests

---

## 🎯 Step 8: Run Examples

### View and Run Examples:

1. **Open `example_usage.py`** from the Explorer
2. Read through the code to understand how it works
3. Click the ▶️ "Run Python File" button

Or in the terminal:
```bash
python example_usage.py
```

This demonstrates:
- How trend analysis works
- How Greeks select optimal strikes
- How trailing stop-loss works
- Complete trading workflow

---

## 🚀 Step 9: Run the Trading System

### For Single Analysis:

1. **Ensure schedule is disabled** in `config.json`:
   ```json
   "schedule": {
     "enabled": false
   }
   ```

2. **Open `main.py`** in VS Code

3. **Run the file**:
   - Click the ▶️ button, or
   - In terminal: `python main.py`

### For Continuous Trading:

1. **Enable schedule** in `config.json`:
   ```json
   "schedule": {
     "enabled": true,
     "start_time": "09:20",
     "end_time": "15:20",
     "check_interval_minutes": 5
   }
   ```

2. **Run `main.py`**

3. **Monitor in VS Code**:
   - The terminal will show live updates
   - Logs are written to `trading.log`

### To Stop:
- Press `Ctrl+C` in the terminal

---

## 📊 Step 10: Monitor Logs in VS Code

### View Trading Log:

1. **Open `trading.log`** from Explorer (it's created after first run)
2. VS Code will show the log file with syntax highlighting
3. The file auto-refreshes when new logs are written

### Live Log Monitoring:

**Option 1 - Using Terminal**:
```bash
# Windows (PowerShell terminal)
Get-Content trading.log -Wait -Tail 50

# Mac/Linux (or Windows Git Bash)
tail -f trading.log
```

**Option 2 - Using Extension**:
- Install "Log Viewer" extension
- Right-click `trading.log` → "Open with Log Viewer"

### Search Logs in VS Code:

1. Open `trading.log`
2. Press `Ctrl+F` (or `Cmd+F`)
3. Search for:
   - `Signal:` - Find all trading signals
   - `BUY_CE` - Find call option entries
   - `BUY_PE` - Find put option entries
   - `NIFTY` - Find NIFTY trades

---

## 🔧 VS Code Tips for This Project

### Debugging:

1. **Set Breakpoints**:
   - Click in the gutter (left of line numbers) to add breakpoint
   - Red dot appears

2. **Start Debugging**:
   - Press `F5` or click "Run and Debug" in sidebar
   - Select "Python File"
   - Code will pause at breakpoints

3. **Debug Controls**:
   - `F10` - Step over
   - `F11` - Step into
   - `Shift+F11` - Step out
   - `F5` - Continue

### Code Navigation:

- **Go to Definition**: `F12` (jump to where function is defined)
- **Go to References**: `Shift+F12` (find where function is used)
- **Go to Symbol**: `Ctrl+Shift+O` (jump to functions in current file)
- **Go to File**: `Ctrl+P` (quick file search)

### Multi-File Editing:

1. **Split Editor**:
   - `Ctrl+\` to split vertically
   - Drag files to different panes
   - Good for viewing `main.py` and `config.json` side-by-side

2. **Multiple Cursors**:
   - `Alt+Click` to add cursors
   - `Ctrl+Alt+Down/Up` to add cursor above/below
   - Useful for editing multiple symbols at once

### Terminal Tips:

- **Multiple Terminals**: Click `+` in terminal panel
- **Split Terminal**: Click split icon in terminal
- **Clear Terminal**: Type `clear` (Mac/Linux) or `cls` (Windows)
- **Previous Command**: Press `↑` arrow key

---

## 🗂️ Recommended VS Code Workspace Layout

### Optimal Layout for Trading:

1. **Left Sidebar**: Explorer (file tree)
   - Quick access to config files
   - View logs

2. **Center**: Editor
   - `main.py` in one tab
   - `config.json` in another
   - Split view if needed

3. **Bottom**: Terminal
   - Run commands
   - Monitor live output

4. **Right Side** (optional): 
   - Problems panel (shows errors/warnings)
   - Output panel (Python extension output)

### Save Your Layout:

1. `File` → `Save Workspace As...`
2. Name it "Algo Trading"
3. Next time: `File` → `Open Workspace...`

---

## 🎨 Customize VS Code for Trading

### Theme Recommendations:

Good themes for long coding/monitoring sessions:

1. **Dark Themes** (easier on eyes):
   - `Ctrl+K Ctrl+T` → Select theme
   - Try: "Dark+ (default)", "Monokai", "Dracula"

2. **Light Themes**:
   - "Light+ (default)", "Solarized Light"

### Font Settings:

For better code readability:

1. `File` → `Preferences` → `Settings` (or `Ctrl+,`)
2. Search for "Font Size"
3. Increase to 14-16 for comfortable viewing
4. Search for "Font Family"
5. Try: "Fira Code", "Consolas", "Monaco"

### Enable Format on Save:

1. Settings (`Ctrl+,`)
2. Search "Format On Save"
3. Check the box
4. Your code will auto-format when you save

---

## 📝 VS Code Keyboard Shortcuts Cheat Sheet

### Essential Shortcuts:

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Command Palette | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Quick Open File | `Ctrl+P` | `Cmd+P` |
| Toggle Terminal | `` Ctrl+` `` | `` Ctrl+` `` |
| Save | `Ctrl+S` | `Cmd+S` |
| Save All | `Ctrl+K S` | `Cmd+Alt+S` |
| Find | `Ctrl+F` | `Cmd+F` |
| Find in Files | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| Run Python File | `Ctrl+Alt+N` | `Cmd+Alt+N` |
| Toggle Sidebar | `Ctrl+B` | `Cmd+B` |
| Split Editor | `Ctrl+\` | `Cmd+\` |

---

## 🔍 Troubleshooting in VS Code

### Issue 1: "Python not found"

**Solution**:
1. Open Command Palette (`Ctrl+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose Python 3.8+
4. Restart VS Code if needed

### Issue 2: "Module not found" errors

**Solution**:
1. Ensure you're in the project folder
2. Check bottom-left corner shows correct Python interpreter
3. Run in terminal: `pip install -r requirements.txt`
4. Reload VS Code: `Ctrl+Shift+P` → "Developer: Reload Window"

### Issue 3: IntelliSense not working

**Solution**:
1. Install Pylance extension
2. Settings → Search "Python Language Server"
3. Set to "Pylance"
4. Reload window

### Issue 4: Git not detected

**Solution**:
1. Install Git: https://git-scm.com/downloads
2. Restart VS Code
3. `File` → `Preferences` → `Settings`
4. Search "Git Path"
5. Point to Git executable if needed

---

## 🎓 Learning Resources

### VS Code Documentation:

- Getting Started: https://code.visualstudio.com/docs
- Python in VS Code: https://code.visualstudio.com/docs/python/python-tutorial
- Debugging: https://code.visualstudio.com/docs/editor/debugging

### Project Documentation:

- `TRADING_README.md` - Full system docs
- `INDICATORS_GUIDE.md` - How indicators work
- `GREEKS_WITH_INDICATORS.md` - How Greeks work
- `LOCAL_SETUP_GUIDE.md` - General setup

---

## ✅ VS Code Setup Checklist

Before trading, ensure:

- [ ] VS Code installed
- [ ] Python extension installed
- [ ] Python 3.8+ selected as interpreter
- [ ] Project cloned/downloaded and opened in VS Code
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `config.json` created with Fyers credentials
- [ ] Tests passing (`python test_system.py`)
- [ ] Examples reviewed (`python example_usage.py`)

---

## 💡 Pro Tips for VS Code

### 1. Use Tasks for Common Commands

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Tests",
      "type": "shell",
      "command": "python test_system.py",
      "group": "test"
    },
    {
      "label": "Run Trading System",
      "type": "shell",
      "command": "python main.py",
      "group": "build"
    },
    {
      "label": "Run Examples",
      "type": "shell",
      "command": "python example_usage.py"
    }
  ]
}
```

Then: `Ctrl+Shift+P` → "Tasks: Run Task" → Select task

### 2. Use Snippets

Create code snippets for common patterns:
- `File` → `Preferences` → `User Snippets`
- Select "Python"
- Add custom snippets for your trading code

### 3. Use Extensions for Better Experience

- **Python Docstring Generator**: Auto-generate docstrings
- **Better Comments**: Highlight different comment types
- **Error Lens**: Inline error messages
- **GitLens**: Enhanced Git capabilities

---

## 🎉 You're Ready!

Your VS Code environment is now set up for algorithmic trading!

**Next Steps**:
1. Run tests to verify everything works
2. Review examples to understand the system
3. Start with paper trading (schedule disabled)
4. Monitor logs and learn from the signals
5. Gradually move to live trading

**Happy Trading! 📈**

---

*For general setup without VS Code specifics, see `LOCAL_SETUP_GUIDE.md`*
