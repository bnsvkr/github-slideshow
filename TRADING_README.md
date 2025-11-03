# NSE Options Algo Trading System

A world-class algorithmic trading system for NSE stocks and Nifty50 using the Fyers API. This system uses advanced technical indicators to identify trends and Options Greeks to select optimal CE (Call) or PE (Put) strikes with moderate risk. Features include trailing stop-loss and dynamic target adjustment.

## Features

### 🎯 Core Capabilities

- **Multi-Indicator Trend Analysis**: Uses world-class indicators including:
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - ADX (Average Directional Index) with +DI/-DI
  - Supertrend
  - EMA (Exponential Moving Averages: 20, 50, 200)
  - Bollinger Bands
  - Stochastic Oscillator
  - ATR (Average True Range)

- **Options Greeks Calculator**: 
  - Delta (price sensitivity)
  - Gamma (delta sensitivity)
  - Theta (time decay)
  - Vega (volatility sensitivity)
  - Intelligent strike selection based on risk tolerance

- **Advanced Risk Management**:
  - Trailing stop-loss that moves with price
  - Dynamic target adjustment based on trend strength
  - Automatic position sizing
  - Moderate risk strike selection using Greeks

- **Automated Trading**:
  - Scheduled trading during market hours
  - Continuous monitoring of positions
  - Automatic order execution (when configured)
  - Real-time position tracking

## System Architecture

```
algo_trading/
├── core/
│   └── fyers_client.py          # Fyers API integration
├── indicators/
│   ├── technical_indicators.py   # Technical analysis
│   └── options_greeks.py         # Options Greeks calculator
├── strategies/
│   ├── options_strategy.py       # Main trading strategy
│   └── risk_management.py        # Trailing SL and targets
└── utils/
    └── config.py                 # Configuration management
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Fyers trading account with API access
- pip package manager

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd github-slideshow
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the system**:
   ```bash
   python main.py
   ```
   This will create a `config.example.json` file on first run.

4. **Setup your configuration**:
   ```bash
   cp config.example.json config.json
   ```
   
   Edit `config.json` and add your Fyers credentials:
   ```json
   {
     "fyers": {
       "client_id": "YOUR_CLIENT_ID",
       "access_token": "YOUR_ACCESS_TOKEN",
       "redirect_uri": "https://your-redirect-uri.com"
     }
   }
   ```

## Configuration

### Fyers API Setup

To get your Fyers API credentials:

1. Log in to your Fyers account
2. Go to API Dashboard
3. Create a new app to get Client ID
4. Generate access token using OAuth2 flow

### Trading Configuration

Key configuration parameters in `config.json`:

```json
{
  "trading": {
    "symbols": [
      "NSE:NIFTY50-INDEX",
      "NSE:BANKNIFTY-INDEX",
      "NSE:SBIN-EQ",
      "NSE:RELIANCE-EQ"
    ],
    "risk_free_rate": 0.065,
    "volatility_default": 0.20,
    "risk_tolerance": "moderate",
    "initial_stop_loss_pct": 2.0,
    "initial_target_pct": 5.0,
    "trailing_stop_pct": 1.5,
    "target_trail_increment_pct": 2.0,
    "max_positions": 5,
    "position_size": 1,
    "time_to_expiry_days": 7
  }
}
```

**Parameters explained**:
- `symbols`: List of instruments to trade
- `risk_free_rate`: Annual risk-free rate (default: 6.5%)
- `volatility_default`: Default volatility if historical data unavailable (20%)
- `risk_tolerance`: Risk level - "low", "moderate", or "high"
- `initial_stop_loss_pct`: Initial stop-loss percentage
- `initial_target_pct`: Initial profit target percentage
- `trailing_stop_pct`: Trailing stop-loss percentage
- `target_trail_increment_pct`: How much to move target up/down
- `max_positions`: Maximum concurrent positions
- `position_size`: Number of lots per trade
- `time_to_expiry_days`: Preferred option expiry days

### Schedule Configuration

```json
{
  "schedule": {
    "enabled": true,
    "start_time": "09:20",
    "end_time": "15:20",
    "check_interval_minutes": 5,
    "trading_days": ["MON", "TUE", "WED", "THU", "FRI"]
  }
}
```

## Usage

### Running the System

**Single run mode** (schedule disabled):
```bash
python main.py
```

**Continuous mode** (schedule enabled):
```bash
python main.py
```

The system will:
1. Analyze trends for all configured symbols
2. Generate trading signals (BUY_CE or BUY_PE)
3. Select optimal strikes using Greeks
4. Execute trades (when configured)
5. Monitor positions with trailing stop-loss
6. Adjust targets based on trend strength

### Understanding the Trading Logic

#### 1. Trend Identification

The system analyzes multiple indicators and scores the trend:

- **Bullish signals** → BUY CALL (CE)
- **Bearish signals** → BUY PUT (PE)
- **Neutral** → NO SIGNAL

Trend strength must be > 50% for signal generation.

#### 2. Strike Selection

Uses Options Greeks to select optimal strike:

- **Low Risk**: Delta ~0.4, lower gamma exposure
- **Moderate Risk**: Delta ~0.5, balanced Greeks
- **High Risk**: Delta ~0.7, higher directional exposure

The system automatically selects ATM/OTM/ITM strikes based on:
- Delta for directional exposure
- Gamma for position stability
- Theta for time decay impact
- Vega for volatility sensitivity

#### 3. Risk Management

**Entry**:
- Initial stop-loss: 2% below entry (for CE) or above (for PE)
- Initial target: 5% profit

**During Trade**:
- **Trailing Stop-Loss**: Moves with price (1.5% trailing)
- **Dynamic Target**: Adjusts upward if trend strengthens
- **Exit Conditions**:
  - Stop-loss hit
  - Target hit with weakening trend
  - Trend reversal

### Monitoring Positions

The system logs all activity to:
- Console (if enabled)
- `trading.log` file

Log entries include:
- Trading signals generated
- Strikes selected with Greeks
- Position entries and exits
- Stop-loss and target updates
- Errors and warnings

## Strategy Details

### Indicators Used

1. **RSI (14)**: Identifies overbought/oversold conditions
2. **MACD (12, 26, 9)**: Trend direction and momentum
3. **ADX (14)**: Trend strength measurement
4. **Supertrend (10, 3)**: Support/resistance levels
5. **EMA (20, 50, 200)**: Trend confirmation
6. **Bollinger Bands**: Volatility and price extremes
7. **Stochastic**: Momentum oscillator
8. **ATR**: Volatility measurement

### Greeks Calculations

Uses Black-Scholes model for European options:

- **Delta**: Rate of change of option price vs. spot price
- **Gamma**: Rate of change of Delta vs. spot price
- **Theta**: Time decay (per day)
- **Vega**: Sensitivity to volatility changes

### Risk Scoring

Each strike is scored based on:
```
risk_score = |delta - target_delta| + gamma_weight * gamma + theta_weight * theta
```

Lower risk score = better strike for risk tolerance.

## Example Workflow

1. **Market Open**: System starts at 09:20
2. **Analysis**: Checks NIFTY50, BANKNIFTY, selected stocks
3. **Signal Generation**:
   - NIFTY50 shows strong bullish trend (strength: 75%)
   - Signal: BUY_CE
4. **Strike Selection**:
   - Spot: 21,500
   - Selected Strike: 21,600 (slightly OTM)
   - Delta: 0.52, Gamma: 0.0008, Theta: -15/day
5. **Position Entry**:
   - Entry Price: ₹150
   - Stop-Loss: ₹147 (2% down)
   - Target: ₹157.50 (5% up)
6. **Monitoring**:
   - Price moves to ₹160
   - Stop-loss trails to ₹157.50
   - Target moves to ₹165
7. **Exit**:
   - Either stop-loss hit or target reached
   - Position closed automatically

## Safety and Risk Warnings

⚠️ **Important Disclaimers**:

1. **Testing Required**: Test thoroughly in paper trading mode before live trading
2. **Market Risk**: Options trading involves substantial risk of loss
3. **Capital Risk**: Only trade with money you can afford to lose
4. **API Limits**: Respect Fyers API rate limits
5. **Network**: Ensure stable internet connection
6. **Monitoring**: Monitor system regularly during trading hours
7. **Backtesting**: Backtest strategies before deployment

## Troubleshooting

### Common Issues

1. **Authentication Error**:
   - Verify Fyers credentials in config.json
   - Check access token is valid and not expired

2. **No Trading Signals**:
   - Check if symbols are correct
   - Verify market data is being fetched
   - Review trend strength threshold

3. **Position Not Opening**:
   - Check available margin
   - Verify symbol format
   - Review order placement logs

4. **System Not Running**:
   - Check schedule configuration
   - Verify current time is within trading hours
   - Check log files for errors

### Logs

Check `trading.log` for detailed information:
```bash
tail -f trading.log
```

## Advanced Features

### Custom Indicators

Add your own indicators in `algo_trading/indicators/technical_indicators.py`:

```python
@staticmethod
def calculate_custom_indicator(data: pd.Series, period: int) -> pd.Series:
    # Your implementation
    return result
```

### Custom Strike Selection

Modify strike selection logic in `algo_trading/indicators/options_greeks.py`:

```python
def select_optimal_strike(...):
    # Custom selection logic
    pass
```

## Performance Optimization

- Historical data is cached (1-hour expiry)
- Parallel signal generation for multiple symbols
- Efficient Greeks calculation
- Minimal API calls

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues and questions:
- Create an issue in the repository
- Check existing documentation
- Review Fyers API documentation

## Disclaimer

This software is for educational and research purposes only. The developers are not responsible for any financial losses incurred through the use of this system. Always conduct thorough testing and risk assessment before deploying any automated trading system with real money.

**Trading in options involves significant risk and may not be suitable for all investors. Past performance is not indicative of future results.**

## Version History

### v1.0.0 (Current)
- Initial release
- Multi-indicator trend analysis
- Options Greeks calculator
- Trailing stop-loss and dynamic targets
- Fyers API integration
- Configurable risk management

---

**Happy Trading! 📈**

Remember: The best trade is a well-researched trade. Always stay informed and trade responsibly.
