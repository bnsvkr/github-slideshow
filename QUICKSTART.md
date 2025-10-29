# Quick Start Guide - NSE Options Trading System

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- numpy (numerical computing)
- pandas (data analysis)
- scipy (scientific computing, for Greeks calculations)
- requests (API calls to Fyers)

### Step 2: Get Fyers API Credentials

1. **Sign up** for a Fyers trading account at https://fyers.in
2. **Create an API App**:
   - Login to Fyers
   - Go to API Dashboard
   - Create new App
   - Note down your **Client ID**
3. **Generate Access Token**:
   - Follow Fyers OAuth2 flow
   - Get your **Access Token**

### Step 3: Configure the System

```bash
# Copy example configuration
cp config.example.json config.json

# Edit configuration with your credentials
nano config.json
```

Update these fields in `config.json`:
```json
{
  "fyers": {
    "client_id": "YOUR_FYERS_CLIENT_ID",
    "access_token": "YOUR_FYERS_ACCESS_TOKEN",
    "redirect_uri": "https://your-redirect-uri.com"
  },
  "trading": {
    "symbols": ["NSE:NIFTY50-INDEX", "NSE:BANKNIFTY-INDEX"]
  }
}
```

**Note**: Only `client_id` and `access_token` are required. Other settings can use defaults from `config.example.json`.

### Step 4: Test the System

```bash
# Run component tests
python test_system.py

# Run usage examples
python example_usage.py
```

### Step 5: Start Trading

**For a single run** (set `"enabled": false` in schedule config):
```bash
python main.py
```
This will analyze trends, generate signals, and exit.

**For continuous trading** (set `"enabled": true` in schedule config):
```bash
python main.py
```
This will run continuously during configured market hours, checking at regular intervals.

## Understanding the Output

### Trading Signals

The system generates three types of signals:

1. **BUY_CE** (Buy Call): When bullish trend is detected
   - Strong upward momentum
   - Multiple indicators confirming uptrend
   - Trend strength > 50%

2. **BUY_PE** (Buy Put): When bearish trend is detected
   - Strong downward momentum
   - Multiple indicators confirming downtrend
   - Trend strength > 50%

3. **NO_SIGNAL**: When trend is unclear or weak
   - Mixed signals from indicators
   - Low trend strength
   - Sideways market

### Log Output Example

```
YYYY-MM-DD 09:25:00 - Running strategy at YYYY-MM-DD 09:25:00
YYYY-MM-DD 09:25:05 - Signal: BUY_CE for NSE:NIFTY50-INDEX
YYYY-MM-DD 09:25:05 -   Trend: STRONG_BULLISH (strength: 75.00)
YYYY-MM-DD 09:25:05 -   Optimal Strike: 21600
YYYY-MM-DD 09:25:05 -   Greeks: {'delta': 0.52, 'gamma': 0.0008, 'theta': -15.5}
YYYY-MM-DD 09:25:06 - Position: BUY_CE - NSE:NIFTY50-INDEX
YYYY-MM-DD 09:25:06 -   Strike: 21600, Entry: 150.00
```

## What Happens Behind the Scenes

### 1. Data Collection
- Fetches historical data for each symbol (365 days)
- Retrieves current market quotes
- Gets option chain data

### 2. Technical Analysis
System calculates 8 major indicators:
- **RSI (14)**: Momentum indicator
- **MACD (12,26,9)**: Trend and momentum
- **ADX (14)**: Trend strength
- **Supertrend (10,3)**: Dynamic support/resistance
- **EMA (20, 50, 200)**: Moving averages
- **Bollinger Bands**: Volatility
- **Stochastic**: Overbought/oversold
- **ATR**: Volatility measurement

### 3. Signal Generation
Scoring system counts:
- Bullish signals (0-10)
- Bearish signals (0-10)

Trend strength = |bullish - bearish| / total * 100%

### 4. Strike Selection
For each available strike:
1. Calculate all Greeks (Delta, Gamma, Theta, Vega)
2. Compute risk score based on:
   - Delta deviation from target
   - Gamma exposure
   - Theta (time decay)
3. Select strike with lowest risk score

### 5. Position Management
After entry:
- Monitor price continuously
- Update trailing stop-loss
- Adjust targets based on trend
- Exit on stop-loss hit or target reached

## Key Configuration Parameters

### Risk Settings

```json
{
  "risk_tolerance": "moderate",      // low, moderate, high
  "initial_stop_loss_pct": 2.0,     // 2% initial stop-loss
  "initial_target_pct": 5.0,        // 5% profit target
  "trailing_stop_pct": 1.5          // 1.5% trailing stop
}
```

**Low Risk**:
- Delta target: 0.4 (40% directional exposure)
- Lower gamma, lower volatility sensitivity
- Tighter stops

**Moderate Risk** (recommended):
- Delta target: 0.5 (50% directional exposure)
- Balanced Greeks
- Standard stops

**High Risk**:
- Delta target: 0.7 (70% directional exposure)
- Higher gamma, more aggressive
- Wider stops

### Trading Schedule

```json
{
  "schedule": {
    "enabled": true,
    "start_time": "09:20",           // After market open
    "end_time": "15:20",             // Before market close
    "check_interval_minutes": 5      // Check every 5 minutes
  }
}
```

## Common Use Cases

### 1. Intraday Trading
```json
{
  "time_to_expiry_days": 0,          // Current day expiry
  "initial_stop_loss_pct": 1.5,     // Tight stop
  "initial_target_pct": 3.0,        // Quick target
  "check_interval_minutes": 1        // Frequent checks
}
```

### 2. Swing Trading
```json
{
  "time_to_expiry_days": 7,          // Weekly expiry
  "initial_stop_loss_pct": 3.0,     // Wider stop
  "initial_target_pct": 8.0,        // Higher target
  "check_interval_minutes": 30       // Less frequent checks
}
```

### 3. Conservative Trading
```json
{
  "risk_tolerance": "low",
  "initial_stop_loss_pct": 2.0,
  "initial_target_pct": 4.0,
  "max_positions": 2                 // Fewer positions
}
```

## Monitoring Your Trades

### Check Logs
```bash
# Live monitoring
tail -f trading.log

# Search for specific symbol
grep "NIFTY50" trading.log

# Check only signals
grep "Signal:" trading.log
```

### Log Files
- `trading.log`: All trading activity
- Console output: Real-time status (if enabled)

## Safety Checklist

Before running with real money:

- [ ] Tested with paper trading
- [ ] Verified API credentials
- [ ] Set appropriate position size
- [ ] Configured risk parameters
- [ ] Understood all indicators
- [ ] Reviewed stop-loss levels
- [ ] Checked available margin
- [ ] Tested during market hours
- [ ] Reviewed trading costs
- [ ] Have backup plan for failures

## Troubleshooting

### No signals generated
**Possible reasons**:
- Market is sideways (no clear trend)
- Trend strength < 50%
- Not enough historical data

**Solution**: Check logs for indicator values, verify data is being fetched

### API errors
**Possible reasons**:
- Invalid credentials
- Expired access token
- Rate limit exceeded

**Solution**: Regenerate access token, reduce check frequency

### Position not opening
**Possible reasons**:
- Insufficient margin
- Invalid symbol format
- Market closed

**Solution**: Verify account balance, check symbol format, ensure trading hours

## Getting Help

1. **Check logs**: `trading.log` has detailed error messages
2. **Run tests**: `python test_system.py` to verify setup
3. **Review examples**: `python example_usage.py` for demonstrations
4. **Read documentation**: `TRADING_README.md` for comprehensive guide

## Next Steps

Once comfortable with the basics:

1. **Backtest strategies**: Test on historical data
2. **Customize indicators**: Add your own technical analysis
3. **Adjust risk parameters**: Fine-tune for your style
4. **Monitor performance**: Track win rate and P&L
5. **Scale gradually**: Start small, increase position size over time

## Important Reminders

⚠️ **Risk Warning**:
- Options trading involves substantial risk
- Past performance doesn't guarantee future results
- Only trade with money you can afford to lose
- Monitor positions during market hours
- Have a clear exit strategy

✅ **Best Practices**:
- Start with small position sizes
- Test thoroughly before going live
- Keep good records of all trades
- Review and learn from each trade
- Stay disciplined with your strategy

---

**Ready to start?** Run `python main.py` and happy trading! 🚀
