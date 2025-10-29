"""
Main Trading Strategy Orchestrator
Combines indicators, Greeks, and risk management for options trading
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from algo_trading.core.fyers_client import FyersAPIClient
from algo_trading.indicators.technical_indicators import TechnicalIndicators, TrendDirection
from algo_trading.indicators.options_greeks import OptionsGreeks
from algo_trading.strategies.risk_management import (
    PositionManager, PositionDirection, TrailingStopLoss
)


class OptionsStrategy:
    """
    Options trading strategy for NSE stocks and Nifty50
    Uses technical indicators and Greeks for CE/PE selection
    """
    
    def __init__(
        self,
        fyers_client: FyersAPIClient,
        symbols: List[str],
        risk_free_rate: float = 0.065,  # 6.5% annual
        volatility_default: float = 0.20,  # 20% annual
        risk_tolerance: str = 'moderate',
        initial_stop_loss_pct: float = 2.0,
        initial_target_pct: float = 5.0,
        trailing_stop_pct: float = 1.5
    ):
        """
        Initialize options trading strategy
        
        Args:
            fyers_client: Fyers API client instance
            symbols: List of symbols to trade
            risk_free_rate: Risk-free interest rate (annual)
            volatility_default: Default volatility if not available
            risk_tolerance: Risk tolerance ('low', 'moderate', 'high')
            initial_stop_loss_pct: Initial stop-loss percentage
            initial_target_pct: Initial target percentage
            trailing_stop_pct: Trailing stop percentage
        """
        self.fyers_client = fyers_client
        self.symbols = symbols
        self.risk_free_rate = risk_free_rate
        self.volatility_default = volatility_default
        self.risk_tolerance = risk_tolerance
        self.initial_stop_loss_pct = initial_stop_loss_pct
        self.initial_target_pct = initial_target_pct
        self.trailing_stop_pct = trailing_stop_pct
        
        self.position_manager = PositionManager()
        self.logger = logging.getLogger(__name__)
        
        # Cache for historical data
        self.historical_data_cache: Dict[str, pd.DataFrame] = {}
        self.last_cache_update: Dict[str, datetime] = {}
    
    def get_historical_data(
        self,
        symbol: str,
        resolution: str = "D",
        days_back: int = 365,
        force_refresh: bool = False
    ) -> Optional[pd.DataFrame]:
        """
        Get historical data with caching
        
        Args:
            symbol: Trading symbol
            resolution: Time resolution
            days_back: Number of days to fetch
            force_refresh: Force refresh cache
            
        Returns:
            DataFrame with OHLC data or None
        """
        cache_key = f"{symbol}_{resolution}"
        
        # Check cache
        if not force_refresh and cache_key in self.historical_data_cache:
            last_update = self.last_cache_update.get(cache_key)
            if last_update and (datetime.now() - last_update).total_seconds() < 3600:
                return self.historical_data_cache[cache_key]
        
        # Fetch new data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        response = self.fyers_client.get_historical_data(
            symbol=symbol,
            resolution=resolution,
            start_date=start_date,
            end_date=end_date
        )
        
        if response.get('s') == 'ok' and 'candles' in response:
            candles = response['candles']
            df = pd.DataFrame(
                candles,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('timestamp', inplace=True)
            
            # Cache the data
            self.historical_data_cache[cache_key] = df
            self.last_cache_update[cache_key] = datetime.now()
            
            return df
        else:
            self.logger.error(f"Failed to fetch historical data for {symbol}")
            return None
    
    def analyze_trend(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Analyze trend for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Trend analysis dictionary or None
        """
        df = self.get_historical_data(symbol)
        if df is None or len(df) < 200:
            self.logger.error(f"Insufficient data for {symbol}")
            return None
        
        trend_analysis = TechnicalIndicators.identify_trend(df)
        return trend_analysis
    
    def get_option_strikes(
        self,
        symbol: str,
        spot_price: float,
        option_type: str = 'call',
        num_strikes: int = 10
    ) -> List[float]:
        """
        Get available option strikes around spot price
        
        Args:
            symbol: Underlying symbol
            spot_price: Current spot price
            option_type: 'call' or 'put'
            num_strikes: Number of strikes to return
            
        Returns:
            List of strike prices
        """
        # For NSE, strikes are typically in increments
        # Nifty50: 50 point increments
        # Bank Nifty: 100 point increments
        # Stocks: varies
        
        if 'NIFTY' in symbol.upper():
            if 'BANK' in symbol.upper():
                increment = 100
            else:
                increment = 50
        else:
            # For stocks, use 2.5% increments
            increment = round(spot_price * 0.025 / 10) * 10
        
        strikes = []
        base_strike = round(spot_price / increment) * increment
        
        # Generate strikes around spot
        for i in range(-num_strikes // 2, num_strikes // 2 + 1):
            strikes.append(base_strike + (i * increment))
        
        return sorted([s for s in strikes if s > 0])
    
    def select_best_strike(
        self,
        symbol: str,
        spot_price: float,
        option_type: str,
        time_to_expiry_days: int = 7
    ) -> Optional[Dict[str, Any]]:
        """
        Select best strike using Greeks
        
        Args:
            symbol: Underlying symbol
            spot_price: Current spot price
            option_type: 'call' or 'put'
            time_to_expiry_days: Days to expiry
            
        Returns:
            Dictionary with optimal strike and Greeks
        """
        strikes = self.get_option_strikes(symbol, spot_price, option_type)
        time_to_expiry = time_to_expiry_days / 365.0
        
        # Use historical volatility or default
        df = self.get_historical_data(symbol, resolution="D", days_back=30)
        if df is not None and len(df) > 20:
            returns = np.log(df['close'] / df['close'].shift(1))
            volatility = returns.std() * np.sqrt(252)  # Annualized
        else:
            volatility = self.volatility_default
        
        optimal = OptionsGreeks.select_optimal_strike(
            spot_price=spot_price,
            strikes=strikes,
            time_to_expiry=time_to_expiry,
            risk_free_rate=self.risk_free_rate,
            volatility=volatility,
            option_type=option_type,
            risk_tolerance=self.risk_tolerance
        )
        
        return optimal
    
    def generate_trading_signal(self, symbol: str) -> Dict[str, Any]:
        """
        Generate trading signal for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Dictionary with trading signal
        """
        # Analyze trend
        trend_analysis = self.analyze_trend(symbol)
        if trend_analysis is None:
            return {'signal': 'NO_SIGNAL', 'reason': 'Insufficient data'}
        
        # Get current price
        quotes = self.fyers_client.get_quotes([symbol])
        if not quotes or 'd' not in quotes:
            return {'signal': 'NO_SIGNAL', 'reason': 'Failed to fetch quotes'}
        
        quote_data = quotes['d'][0] if isinstance(quotes['d'], list) else quotes['d']
        spot_price = quote_data.get('v', {}).get('lp', 0)  # Last price
        
        if spot_price == 0:
            return {'signal': 'NO_SIGNAL', 'reason': 'Invalid price'}
        
        trend_direction = trend_analysis['trend_direction']
        trend_strength = trend_analysis['trend_strength']
        
        signal_data = {
            'symbol': symbol,
            'spot_price': spot_price,
            'trend_direction': trend_direction.value,
            'trend_strength': trend_strength,
            'signal': 'NO_SIGNAL',
            'option_type': None,
            'strike_info': None
        }
        
        # Generate signal based on trend
        if trend_direction in [TrendDirection.STRONG_BULLISH, TrendDirection.BULLISH]:
            # Buy Call (CE)
            if trend_strength > 50:
                signal_data['signal'] = 'BUY_CE'
                signal_data['option_type'] = 'call'
                
                # Select best strike
                strike_info = self.select_best_strike(
                    symbol, spot_price, 'call', time_to_expiry_days=7
                )
                signal_data['strike_info'] = strike_info
                
        elif trend_direction in [TrendDirection.STRONG_BEARISH, TrendDirection.BEARISH]:
            # Buy Put (PE)
            if trend_strength > 50:
                signal_data['signal'] = 'BUY_PE'
                signal_data['option_type'] = 'put'
                
                # Select best strike
                strike_info = self.select_best_strike(
                    symbol, spot_price, 'put', time_to_expiry_days=7
                )
                signal_data['strike_info'] = strike_info
        
        return signal_data
    
    def execute_trade(
        self,
        signal: Dict[str, Any],
        quantity: int = 1
    ) -> Dict[str, Any]:
        """
        Execute trade based on signal
        
        Args:
            signal: Trading signal dictionary
            quantity: Number of lots to trade
            
        Returns:
            Execution result
        """
        if signal['signal'] == 'NO_SIGNAL':
            return {'status': 'NO_ACTION', 'message': 'No trading signal'}
        
        if signal['strike_info'] is None:
            return {'status': 'ERROR', 'message': 'No strike information'}
        
        symbol = signal['symbol']
        option_type = signal['option_type']
        strike = signal['strike_info']['optimal_strike']
        greeks = signal['strike_info']['greeks']
        
        # Construct option symbol (format may vary by broker)
        # Example: NSE:NIFTY2312221500CE for Nifty 15000 CE expiring on 22 Dec 2023
        # Note: Actual format depends on Fyers API requirements
        
        # For now, log the trade intention
        self.logger.info(f"Trade Signal: {signal['signal']} for {symbol}")
        self.logger.info(f"Strike: {strike}, Greeks: {greeks}")
        
        # Place order (implement actual order placement)
        # order_result = self.fyers_client.place_order(...)
        
        # Add position to manager
        direction = PositionDirection.LONG  # Options are typically bought
        entry_price = greeks['price']
        
        position = self.position_manager.add_position(
            symbol=f"{symbol}_{option_type}_{strike}",
            entry_price=entry_price,
            direction=direction,
            initial_stop_loss_pct=self.initial_stop_loss_pct,
            initial_target_pct=self.initial_target_pct,
            trailing_stop_pct=self.trailing_stop_pct
        )
        
        return {
            'status': 'SUCCESS',
            'signal': signal['signal'],
            'symbol': symbol,
            'option_type': option_type,
            'strike': strike,
            'entry_price': entry_price,
            'greeks': greeks,
            'position_levels': position.get_current_levels()
        }
    
    def monitor_positions(self) -> List[Dict[str, Any]]:
        """
        Monitor all active positions and update stop-loss/targets
        
        Returns:
            List of position updates
        """
        updates = []
        
        for symbol, position in self.position_manager.get_all_positions().items():
            # Get current price (implement actual price fetching)
            # For now, use a placeholder
            current_price = position.current_price
            
            # Get trend strength for the underlying
            # trend_analysis = self.analyze_trend(underlying_symbol)
            # trend_strength = trend_analysis.get('trend_strength', 50)
            trend_strength = 50  # Placeholder
            
            # Update position
            update_result = position.update(current_price, trend_strength)
            
            # Check for exit signals
            should_exit, reason = position.should_exit(current_price, trend_strength)
            
            update_data = {
                'symbol': symbol,
                'update': update_result,
                'should_exit': should_exit,
                'exit_reason': reason
            }
            
            updates.append(update_data)
            
            if should_exit:
                self.logger.info(f"Exit signal for {symbol}: {reason}")
                # Implement actual exit logic
                # self.close_position(symbol)
        
        return updates
    
    def run_strategy(self) -> Dict[str, Any]:
        """
        Run the complete trading strategy
        
        Returns:
            Strategy execution results
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'signals': [],
            'positions': [],
            'errors': []
        }
        
        # Generate signals for all symbols
        for symbol in self.symbols:
            try:
                signal = self.generate_trading_signal(symbol)
                results['signals'].append(signal)
                
                # Execute if signal is strong enough
                if signal['signal'] != 'NO_SIGNAL':
                    execution = self.execute_trade(signal)
                    results['positions'].append(execution)
                    
            except Exception as e:
                error_msg = f"Error processing {symbol}: {str(e)}"
                self.logger.error(error_msg)
                results['errors'].append(error_msg)
        
        # Monitor existing positions
        position_updates = self.monitor_positions()
        
        return results
