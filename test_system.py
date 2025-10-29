#!/usr/bin/env python3
"""
Test script to validate core trading system components
"""

import sys
import numpy as np
import pandas as pd
from datetime import datetime

def test_technical_indicators():
    """Test technical indicators module"""
    print("Testing Technical Indicators...")
    
    from algo_trading.indicators.technical_indicators import TechnicalIndicators, TrendDirection
    
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=250, freq='D')
    prices = 100 + np.cumsum(np.random.randn(250) * 2)
    
    df = pd.DataFrame({
        'open': prices + np.random.randn(250) * 0.5,
        'high': prices + np.abs(np.random.randn(250) * 1.5),
        'low': prices - np.abs(np.random.randn(250) * 1.5),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, 250)
    }, index=dates)
    
    # Test indicators
    rsi = TechnicalIndicators.calculate_rsi(df['close'])
    assert not rsi.isna().all(), "RSI calculation failed"
    print(f"  ✓ RSI calculated: {rsi.iloc[-1]:.2f}")
    
    macd_line, signal_line, histogram = TechnicalIndicators.calculate_macd(df['close'])
    assert not macd_line.isna().all(), "MACD calculation failed"
    print(f"  ✓ MACD calculated: {macd_line.iloc[-1]:.2f}")
    
    adx, pos_di, neg_di = TechnicalIndicators.calculate_adx(df['high'], df['low'], df['close'])
    assert not adx.isna().all(), "ADX calculation failed"
    print(f"  ✓ ADX calculated: {adx.iloc[-1]:.2f}")
    
    # Test trend identification
    trend_analysis = TechnicalIndicators.identify_trend(df)
    assert 'trend_direction' in trend_analysis, "Trend identification failed"
    print(f"  ✓ Trend identified: {trend_analysis['trend_direction'].value}")
    print(f"  ✓ Trend strength: {trend_analysis['trend_strength']:.2f}")
    
    print("✅ Technical Indicators: PASSED\n")
    return True


def test_options_greeks():
    """Test options Greeks calculator"""
    print("Testing Options Greeks Calculator...")
    
    from algo_trading.indicators.options_greeks import OptionsGreeks
    
    # Test parameters
    spot_price = 21500
    strike_price = 21600
    time_to_expiry = 7 / 365  # 7 days
    risk_free_rate = 0.065
    volatility = 0.20
    
    # Test call option
    call_greeks = OptionsGreeks.calculate_all_greeks(
        spot_price, strike_price, time_to_expiry, risk_free_rate, volatility, 'call'
    )
    
    assert 'delta' in call_greeks, "Delta calculation failed"
    assert 0 <= call_greeks['delta'] <= 1, "Call delta out of range"
    print(f"  ✓ Call Delta: {call_greeks['delta']:.4f}")
    print(f"  ✓ Call Gamma: {call_greeks['gamma']:.6f}")
    print(f"  ✓ Call Theta: {call_greeks['theta_daily']:.2f}/day")
    print(f"  ✓ Call Vega: {call_greeks['vega']:.4f}")
    
    # Test put option
    put_greeks = OptionsGreeks.calculate_all_greeks(
        spot_price, strike_price, time_to_expiry, risk_free_rate, volatility, 'put'
    )
    
    assert -1 <= put_greeks['delta'] <= 0, "Put delta out of range"
    print(f"  ✓ Put Delta: {put_greeks['delta']:.4f}")
    
    # Test strike selection
    strikes = [21000, 21200, 21400, 21500, 21600, 21800, 22000]
    optimal = OptionsGreeks.select_optimal_strike(
        spot_price, strikes, time_to_expiry, risk_free_rate, volatility, 'call', 'moderate'
    )
    
    assert 'optimal_strike' in optimal, "Strike selection failed"
    print(f"  ✓ Optimal Strike: {optimal['optimal_strike']}")
    print(f"  ✓ Moneyness: {optimal['moneyness']}")
    
    print("✅ Options Greeks: PASSED\n")
    return True


def test_risk_management():
    """Test risk management module"""
    print("Testing Risk Management...")
    
    from algo_trading.strategies.risk_management import (
        TrailingStopLoss, PositionDirection, PositionManager
    )
    
    # Test trailing stop-loss for long position
    entry_price = 150.0
    tsl = TrailingStopLoss(
        entry_price=entry_price,
        direction=PositionDirection.LONG,
        initial_stop_loss_pct=2.0,
        initial_target_pct=5.0,
        trailing_stop_pct=1.5
    )
    
    assert tsl.stop_loss < entry_price, "Initial stop-loss incorrect for LONG"
    assert tsl.target > entry_price, "Initial target incorrect for LONG"
    print(f"  ✓ Initial Stop-Loss: {tsl.stop_loss:.2f}")
    print(f"  ✓ Initial Target: {tsl.target:.2f}")
    
    # Simulate price movement
    new_price = 160.0
    update = tsl.update(new_price, trend_strength=70)
    
    assert update['stop_loss'] > entry_price, "Trailing stop should move up"
    print(f"  ✓ Trailing Stop updated: {update['stop_loss']:.2f}")
    print(f"  ✓ P&L: {update['pnl_pct']:.2f}%")
    
    # Test position manager
    pm = PositionManager()
    position = pm.add_position(
        symbol="NIFTY_CE_21600",
        entry_price=150.0,
        direction=PositionDirection.LONG
    )
    
    assert position is not None, "Position creation failed"
    assert "NIFTY_CE_21600" in pm.get_all_positions(), "Position not in manager"
    print(f"  ✓ Position added successfully")
    
    # Update position
    update_result = pm.update_position("NIFTY_CE_21600", 155.0, 60)
    assert update_result is not None, "Position update failed"
    print(f"  ✓ Position updated successfully")
    
    print("✅ Risk Management: PASSED\n")
    return True


def test_config_management():
    """Test configuration management"""
    print("Testing Configuration Management...")
    
    from algo_trading.utils.config import ConfigManager
    
    # Create example config
    cm = ConfigManager()
    cm.create_example_config("/tmp/test_config.example.json")
    print(f"  ✓ Example config created")
    
    # Verify file exists
    import os
    assert os.path.exists("/tmp/test_config.example.json"), "Config file not created"
    print(f"  ✓ Config file verified")
    
    print("✅ Configuration Management: PASSED\n")
    return True


def test_fyers_client_structure():
    """Test Fyers client structure (without API calls)"""
    print("Testing Fyers Client Structure...")
    
    from algo_trading.core.fyers_client import FyersAPIClient
    
    # Create client (won't make actual API calls)
    client = FyersAPIClient(
        client_id="TEST_ID",
        access_token="TEST_TOKEN"
    )
    
    assert client.client_id == "TEST_ID", "Client ID not set"
    assert client.access_token == "TEST_TOKEN", "Access token not set"
    print(f"  ✓ Client initialization successful")
    
    print("✅ Fyers Client Structure: PASSED\n")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("NSE Options Trading System - Component Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_technical_indicators,
        test_options_greeks,
        test_risk_management,
        test_config_management,
        test_fyers_client_structure
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__} FAILED: {str(e)}\n")
            failed += 1
            import traceback
            traceback.print_exc()
    
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
