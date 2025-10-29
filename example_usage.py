#!/usr/bin/env python3
"""
Example Usage of NSE Options Trading System
Demonstrates how to use the trading system components
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Import trading system components
from algo_trading.indicators.technical_indicators import TechnicalIndicators, TrendDirection
from algo_trading.indicators.options_greeks import OptionsGreeks
from algo_trading.strategies.risk_management import TrailingStopLoss, PositionDirection


def example_trend_analysis():
    """
    Example: Analyze trend using technical indicators
    """
    print("=" * 80)
    print("Example 1: Trend Analysis with Multiple Indicators")
    print("=" * 80)
    
    # Create sample historical data (simulating NIFTY50)
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=250, freq='D')
    base_price = 21000
    trend = np.linspace(0, 1500, 250)  # Uptrend
    noise = np.random.randn(250) * 100
    prices = base_price + trend + noise
    
    df = pd.DataFrame({
        'open': prices + np.random.randn(250) * 20,
        'high': prices + np.abs(np.random.randn(250) * 50),
        'low': prices - np.abs(np.random.randn(250) * 50),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, 250)
    }, index=dates)
    
    print(f"\nAnalyzing trend for NIFTY50...")
    print(f"Current Price: ₹{df['close'].iloc[-1]:.2f}")
    print(f"Price Range: ₹{df['close'].min():.2f} - ₹{df['close'].max():.2f}")
    
    # Analyze trend
    trend_analysis = TechnicalIndicators.identify_trend(df)
    
    print(f"\n📊 Trend Analysis Results:")
    print(f"  Trend Direction: {trend_analysis['trend_direction'].value}")
    print(f"  Trend Strength: {trend_analysis['trend_strength']:.2f}%")
    print(f"  Bullish Signals: {trend_analysis['bullish_signals']}")
    print(f"  Bearish Signals: {trend_analysis['bearish_signals']}")
    
    print(f"\n📈 Key Indicators:")
    print(f"  RSI: {trend_analysis['rsi']:.2f}")
    print(f"  MACD: {trend_analysis['macd']:.2f}")
    print(f"  ADX: {trend_analysis['adx']:.2f}")
    print(f"  Supertrend: {trend_analysis['supertrend_direction']}")
    
    # Trading decision
    if trend_analysis['trend_direction'] in [TrendDirection.STRONG_BULLISH, TrendDirection.BULLISH]:
        if trend_analysis['trend_strength'] > 50:
            print(f"\n✅ TRADING SIGNAL: BUY CALL (CE)")
            return 'BUY_CE', df['close'].iloc[-1]
    elif trend_analysis['trend_direction'] in [TrendDirection.STRONG_BEARISH, TrendDirection.BEARISH]:
        if trend_analysis['trend_strength'] > 50:
            print(f"\n✅ TRADING SIGNAL: BUY PUT (PE)")
            return 'BUY_PE', df['close'].iloc[-1]
    
    print(f"\n⏸️  TRADING SIGNAL: NO TRADE (Trend not strong enough)")
    return 'NO_SIGNAL', df['close'].iloc[-1]


def example_strike_selection(signal, spot_price):
    """
    Example: Select optimal strike using Options Greeks
    """
    print("\n" + "=" * 80)
    print("Example 2: Options Strike Selection Using Greeks")
    print("=" * 80)
    
    if signal == 'NO_SIGNAL':
        print("\nNo signal to process")
        return
    
    option_type = 'call' if signal == 'BUY_CE' else 'put'
    
    print(f"\nSelecting optimal {option_type.upper()} strike...")
    print(f"Spot Price: ₹{spot_price:.2f}")
    
    # Generate strike prices around spot
    increment = 50  # NIFTY increment
    base_strike = round(spot_price / increment) * increment
    strikes = [base_strike + (i * increment) for i in range(-5, 6)]
    
    print(f"Available Strikes: {strikes}")
    
    # Select optimal strike
    time_to_expiry = 7 / 365  # 7 days
    risk_free_rate = 0.065
    volatility = 0.20
    
    optimal = OptionsGreeks.select_optimal_strike(
        spot_price=spot_price,
        strikes=strikes,
        time_to_expiry=time_to_expiry,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        option_type=option_type,
        risk_tolerance='moderate'
    )
    
    print(f"\n🎯 Optimal Strike Selected: ₹{optimal['optimal_strike']}")
    print(f"   Moneyness: {optimal['moneyness']}")
    print(f"   Risk Score: {optimal['risk_score']:.4f}")
    
    greeks = optimal['greeks']
    print(f"\n📊 Greeks for Selected Strike:")
    print(f"   Price: ₹{greeks['price']:.2f}")
    print(f"   Delta: {greeks['delta']:.4f}")
    print(f"   Gamma: {greeks['gamma']:.6f}")
    print(f"   Theta: {greeks['theta_daily']:.2f}/day")
    print(f"   Vega: {greeks['vega']:.4f}")
    
    print(f"\n💡 What this means:")
    print(f"   - For every ₹1 move in NIFTY, option price changes by ₹{abs(greeks['delta']):.2f}")
    print(f"   - Losing ₹{abs(greeks['theta_daily']):.2f} per day due to time decay")
    print(f"   - For every 1% change in volatility, price changes by ₹{greeks['vega']:.2f}")
    
    # Show top 3 alternatives
    print(f"\n📋 Top 3 Alternative Strikes:")
    for i, alt in enumerate(optimal['all_strikes'][:3], 1):
        print(f"   {i}. Strike ₹{alt['strike']} ({alt['moneyness']})")
        print(f"      Delta: {alt['greeks']['delta']:.4f}, Risk Score: {alt['risk_score']:.4f}")
    
    return optimal['optimal_strike'], greeks['price']


def example_risk_management(entry_price):
    """
    Example: Manage position with trailing stop-loss
    """
    print("\n" + "=" * 80)
    print("Example 3: Risk Management with Trailing Stop-Loss")
    print("=" * 80)
    
    print(f"\nOpening position at ₹{entry_price:.2f}")
    
    # Create trailing stop-loss
    tsl = TrailingStopLoss(
        entry_price=entry_price,
        direction=PositionDirection.LONG,
        initial_stop_loss_pct=2.0,
        initial_target_pct=5.0,
        trailing_stop_pct=1.5,
        target_trail_increment_pct=2.0
    )
    
    print(f"\n📍 Initial Levels:")
    print(f"   Entry: ₹{entry_price:.2f}")
    print(f"   Stop-Loss: ₹{tsl.stop_loss:.2f} (-{((entry_price - tsl.stop_loss)/entry_price)*100:.2f}%)")
    print(f"   Target: ₹{tsl.target:.2f} (+{((tsl.target - entry_price)/entry_price)*100:.2f}%)")
    
    # Simulate price movements
    price_movements = [
        (entry_price * 1.02, 60, "Price moves up 2%"),
        (entry_price * 1.04, 70, "Price moves up 4%"),
        (entry_price * 1.06, 75, "Price moves up 6%"),
        (entry_price * 1.05, 50, "Price retraces to +5%, trend weakens"),
    ]
    
    print(f"\n📈 Price Movement Simulation:")
    for i, (price, trend_strength, description) in enumerate(price_movements, 1):
        print(f"\n   Step {i}: {description}")
        print(f"   Current Price: ₹{price:.2f}")
        
        update = tsl.update(price, trend_strength)
        
        print(f"   Stop-Loss: ₹{update['stop_loss']:.2f}", end="")
        if update['stop_loss_updated']:
            print(" 🔼 UPDATED")
        else:
            print()
        
        print(f"   Target: ₹{update['target']:.2f}", end="")
        if update['target_updated']:
            print(" 🔼 UPDATED")
        else:
            print()
        
        print(f"   P&L: {update['pnl_pct']:.2f}%")
        
        should_exit, reason = tsl.should_exit(price, trend_strength)
        if should_exit:
            print(f"\n   🚨 EXIT SIGNAL: {reason}")
            final_pnl = ((price - entry_price) / entry_price) * 100
            print(f"   Final P&L: {final_pnl:.2f}%")
            break
    else:
        print(f"\n   ✅ Position still active")
    
    print(f"\n💡 Trailing Stop-Loss Benefits:")
    print(f"   - Protects profits as price moves in your favor")
    print(f"   - Automatically adjusts target based on trend strength")
    print(f"   - Locks in gains while allowing for trend continuation")


def main():
    """
    Run all examples
    """
    print("\n" + "=" * 80)
    print("NSE OPTIONS TRADING SYSTEM - USAGE EXAMPLES")
    print("=" * 80)
    
    # Example 1: Trend Analysis
    signal, spot_price = example_trend_analysis()
    
    # Example 2: Strike Selection
    if signal != 'NO_SIGNAL':
        strike, entry_price = example_strike_selection(signal, spot_price)
        
        # Example 3: Risk Management
        example_risk_management(entry_price)
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)
    print("\nNext Steps:")
    print("1. Copy config.example.json to config.json")
    print("2. Add your Fyers API credentials")
    print("3. Run: python main.py")
    print("\nFor more information, see TRADING_README.md")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
