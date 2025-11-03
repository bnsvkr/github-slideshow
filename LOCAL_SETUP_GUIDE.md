# Local Setup Guide - NSE Options Algo Trading System

## Complete Installation Instructions for Windows/Mac/Linux

This guide will help you download and set up the algorithmic trading system on your local PC.

---

## 📥 Step 1: Download the Files

### Option A: Download as ZIP (Easiest)

1. **Go to the GitHub repository**:
   - Open your browser and visit: `https://github.com/bnsvkr/github-slideshow`

2. **Download the ZIP file**:
   - Click the green **"Code"** button (top right)
   - Select **"Download ZIP"**
   - Save the file to your desired location (e.g., `C:\Trading` on Windows or `~/Trading` on Mac/Linux)

3. **Extract the ZIP**:
   - Right-click the downloaded file
   - Select "Extract All..." (Windows) or double-click (Mac)
   - Extract to a folder like `C:\Trading\github-slideshow` or `~/Trading/github-slideshow`

### Option B: Clone with Git (Recommended for developers)

**Prerequisites**: Install Git from https://git-scm.com/downloads

1. **Open Terminal/Command Prompt**:
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - Mac: Press `Cmd + Space`, type `terminal`, press Enter
   - Linux: Press `Ctrl + Alt + T`

2. **Navigate to your desired folder**:
   ```bash
   # Windows
   cd C:\Trading
   
   # Mac/Linux
   cd ~/Trading
   ```

3. **Clone the repository**:
   ```bash
   git clone https://github.com/bnsvkr/github-slideshow.git
   cd github-slideshow
   ```

4. **Switch to the trading branch** (if needed):
   ```bash
   git checkout copilot/create-algo-trading-setup
   ```

---

## 🐍 Step 2: Install Python

### Check if Python is installed:

```bash
python --version
# or
python3 --version
```

If you see `Python 3.8` or higher, you're good! Otherwise:

### Install Python:

**Windows**:
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"

**Mac**:
```bash
# Using Homebrew (recommended)
brew install python3

# Or download from https://www.python.org/downloads/
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Linux (Fedora/RHEL)**:
```bash
sudo dnf install python3 python3-pip
```

---

## 📦 Step 3: Install Required Packages

1. **Navigate to the project folder**:
   ```bash
   # Windows
   cd C:\Trading\github-slideshow
   
   # Mac/Linux
   cd ~/Trading/github-slideshow
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or if the above doesn't work:
   ```bash
   pip3 install -r requirements.txt
   ```

   This will install:
   - `numpy` - Numerical computing
   - `pandas` - Data analysis
   - `scipy` - Scientific computing (for Greeks calculations)
   - `requests` - HTTP library for API calls

**Troubleshooting**:
- If you get "pip not found": Use `python -m pip install -r requirements.txt`
- If you get permission errors on Mac/Linux: Add `--user` flag: `pip3 install --user -r requirements.txt`

---

## 🔑 Step 4: Get Fyers API Credentials

You need a Fyers trading account and API credentials to run the system.

### 4.1 Create Fyers Account

1. Visit https://fyers.in
2. Sign up for a trading account
3. Complete KYC verification
4. Activate your account

### 4.2 Create API App

1. **Login to Fyers**: https://myapi.fyers.in/
2. **Go to "My Apps"** section
3. **Create New App**:
   - App Name: `AlgoTrading` (or any name)
   - App Type: `Web App`
   - Redirect URL: `https://127.0.0.1` (for local testing)
   - Click **"Create"**
4. **Note down**:
   - **App ID** (this is your Client ID)
   - **Secret Key**

### 4.3 Generate Access Token

Fyers uses OAuth2, so you need to generate an access token:

**Option 1 - Use Fyers API Dashboard** (Recommended):
1. Go to https://myapi.fyers.in/generate-access-token
2. Select your app
3. Click "Generate Token"
4. Copy the generated access token

**Option 2 - Manual OAuth Flow** (Advanced):
1. Visit the authorization URL with your credentials
2. Login and approve the app
3. Get the authorization code from redirect URL
4. Exchange code for access token using Fyers API

**Note**: Access tokens expire after a certain time. You'll need to regenerate them periodically.

---

## ⚙️ Step 5: Configure the System

1. **Copy the example configuration**:
   ```bash
   # Windows (Command Prompt)
   copy config.example.json config.json
   
   # Mac/Linux or Windows (PowerShell)
   cp config.example.json config.json
   ```

2. **Edit the configuration file**:
   
   **Windows**:
   ```bash
   notepad config.json
   ```
   
   **Mac**:
   ```bash
   nano config.json
   # or
   open -e config.json
   ```
   
   **Linux**:
   ```bash
   nano config.json
   # or
   gedit config.json
   ```

3. **Update your credentials**:
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
       "initial_target_pct": 5.0
     },
     "schedule": {
       "enabled": false,
       "start_time": "09:20",
       "end_time": "15:20",
       "check_interval_minutes": 5
     }
   }
   ```

4. **Save and close** the file
   - Notepad: `File → Save`
   - Nano: `Ctrl + X`, then `Y`, then `Enter`

---

## ✅ Step 6: Verify Installation

Run the test suite to make sure everything is working:

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
  ✓ ADX calculated: XX.XX
  ✓ Trend identified: BULLISH
✅ Technical Indicators: PASSED

Testing Options Greeks Calculator...
  ✓ Call Delta: 0.XXXX
  ✓ Call Gamma: 0.XXXXXX
  ✓ Optimal Strike: XXXXX
✅ Options Greeks: PASSED

...

Test Results: 5 passed, 0 failed
============================================================
```

---

## 🎯 Step 7: Run Example Demonstrations

Before trading with real money, run the examples to understand how the system works:

```bash
python example_usage.py
```

This will show you:
- How trend analysis works
- How Greeks select optimal strikes
- How trailing stop-loss adjusts
- Complete trading workflow

---

## 🚀 Step 8: Start Trading

### For a Single Analysis Run:

1. **Set schedule to disabled** in `config.json`:
   ```json
   "schedule": {
     "enabled": false
   }
   ```

2. **Run the system**:
   ```bash
   python main.py
   ```

This will:
- Analyze all configured symbols
- Generate trading signals
- Show optimal strikes with Greeks
- Exit after one run

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

2. **Run the system**:
   ```bash
   python main.py
   ```

This will:
- Run continuously during market hours (9:20 AM - 3:20 PM)
- Check signals every 5 minutes
- Log all activity to `trading.log`

### To Stop the System:

Press `Ctrl + C` in the terminal

---

## 📁 Your Folder Structure

After setup, your folder should look like this:

```
github-slideshow/
├── algo_trading/           # Core trading system
│   ├── core/              # Fyers API client
│   ├── indicators/        # Technical indicators & Greeks
│   ├── strategies/        # Trading strategy & risk management
│   └── utils/             # Configuration management
├── main.py                # Main application
├── test_system.py         # Component tests
├── example_usage.py       # Usage examples
├── requirements.txt       # Python dependencies
├── config.example.json    # Example configuration (DO NOT EDIT)
├── config.json           # YOUR configuration (edit this)
├── trading.log           # Trading activity log (created automatically)
├── TRADING_README.md     # Full documentation
├── QUICKSTART.md         # Quick setup guide
├── INDICATORS_GUIDE.md   # How indicators work
└── GREEKS_WITH_INDICATORS.md  # How Greeks work with indicators
```

---

## 📊 Monitoring Your Trades

### View Live Logs:

**Windows (Command Prompt)**:
```bash
type trading.log
# For live monitoring, use PowerShell:
Get-Content trading.log -Wait
```

**Mac/Linux**:
```bash
tail -f trading.log
```

### Check Specific Information:

**Find all signals**:
```bash
# Windows (PowerShell)
Select-String "Signal:" trading.log

# Mac/Linux
grep "Signal:" trading.log
```

**Find NIFTY trades**:
```bash
# Windows (PowerShell)
Select-String "NIFTY" trading.log

# Mac/Linux
grep "NIFTY" trading.log
```

---

## 🔧 Common Issues and Solutions

### Issue 1: "pip not found"

**Solution**:
```bash
python -m pip install -r requirements.txt
# or
python3 -m pip install -r requirements.txt
```

### Issue 2: "ModuleNotFoundError: No module named 'numpy'"

**Solution**:
```bash
pip install numpy pandas scipy requests
```

### Issue 3: "Permission denied" (Mac/Linux)

**Solution**:
```bash
pip3 install --user -r requirements.txt
```

### Issue 4: "config.json not found"

**Solution**:
```bash
# Make sure you copied the example
cp config.example.json config.json
```

### Issue 5: "Invalid Fyers credentials"

**Solutions**:
- Verify your Client ID and Access Token are correct
- Check if access token has expired (regenerate if needed)
- Ensure redirect_uri matches what you set in Fyers dashboard

### Issue 6: Python version too old

**Check version**:
```bash
python --version
```

**Need Python 3.8+**. If you have an older version:
- Windows/Mac: Download latest from https://www.python.org/downloads/
- Linux: `sudo apt install python3.10` (or latest available)

---

## 📚 Next Steps

1. **Read the Documentation**:
   - `TRADING_README.md` - Complete system guide
   - `INDICATORS_GUIDE.md` - How indicators identify entry/exit
   - `GREEKS_WITH_INDICATORS.md` - How Greeks select strikes
   - `QUICKSTART.md` - Quick reference

2. **Start with Paper Trading**:
   - Test the system without real money first
   - Monitor signals and understand the logic
   - Verify it works for your trading style

3. **Customize Configuration**:
   - Adjust risk tolerance (low/moderate/high)
   - Change stop-loss and target percentages
   - Add more symbols to watch

4. **Monitor and Learn**:
   - Review `trading.log` regularly
   - Understand why signals are generated
   - Track performance over time

---

## 🆘 Getting Help

### Check Logs:
```bash
# View last 50 lines of log
tail -n 50 trading.log  # Mac/Linux
Get-Content trading.log -Tail 50  # Windows PowerShell
```

### Common Log Messages:

**"Running strategy at..."** - System is running normally

**"Signal: BUY_CE for NSE:NIFTY50-INDEX"** - Generated a call option signal

**"No trading signal"** - Trend not strong enough, staying out

**"Error fetching..."** - API issue, check internet/credentials

---

## ⚠️ Important Reminders

1. **Start Small**: Test with paper trading before using real money
2. **Check Credentials**: Ensure Fyers API access token is valid
3. **Monitor Regularly**: Watch `trading.log` during market hours
4. **Backup Config**: Keep a copy of your `config.json` settings
5. **Update Token**: Regenerate Fyers access token when it expires
6. **Risk Warning**: Trading involves risk - only trade with money you can afford to lose

---

## 🎓 Learning Resources

**In this repository**:
- `TRADING_README.md` - Full system documentation
- `INDICATORS_GUIDE.md` - Technical indicators explained
- `GREEKS_WITH_INDICATORS.md` - Greeks and strike selection
- `example_usage.py` - Working code examples

**External Resources**:
- Fyers API Documentation: https://myapi.fyers.in/docs/
- Python Tutorial: https://docs.python.org/3/tutorial/
- Options Trading Basics: Search "Options Greeks explained"

---

## ✅ Quick Checklist

Before running the system, ensure:

- [ ] Python 3.8+ installed
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] Fyers account created and verified
- [ ] API app created in Fyers dashboard
- [ ] Access token generated
- [ ] `config.json` created and updated with credentials
- [ ] Tests passing (`python test_system.py`)
- [ ] Examples reviewed (`python example_usage.py`)
- [ ] Documentation read (at least `TRADING_README.md`)

---

## 🎉 You're Ready!

Your algorithmic trading system is now set up and ready to use!

**Remember**: 
- Start with small positions
- Monitor the system closely
- Test thoroughly before deploying with real capital
- Review trades in `trading.log` to learn and improve

**Happy Trading! 📈**

---

*For more detailed information, see `TRADING_README.md` or run `python example_usage.py` for demonstrations.*
