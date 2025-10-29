"""
World-class Technical Indicators for Trend Analysis
Implements multiple indicators for robust trend identification
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any
from enum import Enum


class TrendDirection(Enum):
    """Enum for trend direction"""
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    STRONG_BULLISH = "STRONG_BULLISH"
    STRONG_BEARISH = "STRONG_BEARISH"


class TechnicalIndicators:
    """
    Collection of world-class technical indicators for trend identification
    """
    
    @staticmethod
    def calculate_ema(data: pd.Series, period: int) -> pd.Series:
        """
        Calculate Exponential Moving Average
        
        Args:
            data: Price data series
            period: EMA period
            
        Returns:
            EMA series
        """
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_sma(data: pd.Series, period: int) -> pd.Series:
        """
        Calculate Simple Moving Average
        
        Args:
            data: Price data series
            period: SMA period
            
        Returns:
            SMA series
        """
        return data.rolling(window=period).mean()
    
    @staticmethod
    def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index
        
        Args:
            data: Price data series
            period: RSI period (default 14)
            
        Returns:
            RSI series
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(
        data: pd.Series,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            data: Price data series
            fast_period: Fast EMA period
            slow_period: Slow EMA period
            signal_period: Signal line period
            
        Returns:
            Tuple of (MACD line, Signal line, Histogram)
        """
        ema_fast = TechnicalIndicators.calculate_ema(data, fast_period)
        ema_slow = TechnicalIndicators.calculate_ema(data, slow_period)
        macd_line = ema_fast - ema_slow
        signal_line = TechnicalIndicators.calculate_ema(macd_line, signal_period)
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def calculate_bollinger_bands(
        data: pd.Series,
        period: int = 20,
        num_std: float = 2.0
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate Bollinger Bands
        
        Args:
            data: Price data series
            period: Moving average period
            num_std: Number of standard deviations
            
        Returns:
            Tuple of (Upper band, Middle band, Lower band)
        """
        middle_band = TechnicalIndicators.calculate_sma(data, period)
        std_dev = data.rolling(window=period).std()
        upper_band = middle_band + (std_dev * num_std)
        lower_band = middle_band - (std_dev * num_std)
        
        return upper_band, middle_band, lower_band
    
    @staticmethod
    def calculate_adx(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate Average Directional Index (ADX)
        
        Args:
            high: High price series
            low: Low price series
            close: Close price series
            period: ADX period
            
        Returns:
            Tuple of (ADX, +DI, -DI)
        """
        # Calculate True Range
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        
        # Calculate Directional Movement
        high_diff = high.diff()
        low_diff = -low.diff()
        
        pos_dm = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0)
        neg_dm = low_diff.where((low_diff > high_diff) & (low_diff > 0), 0)
        
        # Smooth True Range and Directional Movement
        atr = tr.rolling(window=period).mean()
        pos_di = 100 * (pos_dm.rolling(window=period).mean() / atr)
        neg_di = 100 * (neg_dm.rolling(window=period).mean() / atr)
        
        # Calculate ADX
        dx = 100 * np.abs(pos_di - neg_di) / (pos_di + neg_di)
        adx = dx.rolling(window=period).mean()
        
        return adx, pos_di, neg_di
    
    @staticmethod
    def calculate_supertrend(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 10,
        multiplier: float = 3.0
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Calculate Supertrend indicator
        
        Args:
            high: High price series
            low: Low price series
            close: Close price series
            period: ATR period
            multiplier: ATR multiplier
            
        Returns:
            Tuple of (Supertrend, Trend direction 1=up, -1=down)
        """
        # Calculate ATR
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        # Calculate basic bands
        hl_avg = (high + low) / 2
        upper_band = hl_avg + (multiplier * atr)
        lower_band = hl_avg - (multiplier * atr)
        
        # Calculate Supertrend
        supertrend = pd.Series(index=close.index, dtype=float)
        direction = pd.Series(index=close.index, dtype=float)
        
        supertrend.iloc[0] = upper_band.iloc[0]
        direction.iloc[0] = 1
        
        for i in range(1, len(close)):
            if close.iloc[i] > supertrend.iloc[i-1]:
                supertrend.iloc[i] = lower_band.iloc[i]
                direction.iloc[i] = 1
            elif close.iloc[i] < supertrend.iloc[i-1]:
                supertrend.iloc[i] = upper_band.iloc[i]
                direction.iloc[i] = -1
            else:
                supertrend.iloc[i] = supertrend.iloc[i-1]
                direction.iloc[i] = direction.iloc[i-1]
                
                if direction.iloc[i] == 1 and lower_band.iloc[i] < supertrend.iloc[i-1]:
                    supertrend.iloc[i] = lower_band.iloc[i]
                elif direction.iloc[i] == -1 and upper_band.iloc[i] > supertrend.iloc[i-1]:
                    supertrend.iloc[i] = upper_band.iloc[i]
        
        return supertrend, direction
    
    @staticmethod
    def calculate_stochastic(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        k_period: int = 14,
        d_period: int = 3
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Calculate Stochastic Oscillator
        
        Args:
            high: High price series
            low: Low price series
            close: Close price series
            k_period: %K period
            d_period: %D period
            
        Returns:
            Tuple of (%K, %D)
        """
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_period).mean()
        
        return k_percent, d_percent
    
    @staticmethod
    def calculate_atr(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14
    ) -> pd.Series:
        """
        Calculate Average True Range
        
        Args:
            high: High price series
            low: Low price series
            close: Close price series
            period: ATR period
            
        Returns:
            ATR series
        """
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr
    
    @staticmethod
    def identify_trend(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Identify overall trend using multiple indicators
        
        Args:
            df: DataFrame with OHLC data (columns: open, high, low, close, volume)
            
        Returns:
            Dictionary with trend analysis
        """
        close = df['close']
        high = df['high']
        low = df['low']
        
        # Calculate indicators
        rsi = TechnicalIndicators.calculate_rsi(close)
        macd_line, signal_line, histogram = TechnicalIndicators.calculate_macd(close)
        adx, pos_di, neg_di = TechnicalIndicators.calculate_adx(high, low, close)
        supertrend, st_direction = TechnicalIndicators.calculate_supertrend(high, low, close)
        ema_20 = TechnicalIndicators.calculate_ema(close, 20)
        ema_50 = TechnicalIndicators.calculate_ema(close, 50)
        ema_200 = TechnicalIndicators.calculate_ema(close, 200)
        
        # Get latest values
        latest_close = close.iloc[-1]
        latest_rsi = rsi.iloc[-1]
        latest_macd = macd_line.iloc[-1]
        latest_signal = signal_line.iloc[-1]
        latest_histogram = histogram.iloc[-1]
        latest_adx = adx.iloc[-1]
        latest_pos_di = pos_di.iloc[-1]
        latest_neg_di = neg_di.iloc[-1]
        latest_st_direction = st_direction.iloc[-1]
        latest_ema_20 = ema_20.iloc[-1]
        latest_ema_50 = ema_50.iloc[-1]
        latest_ema_200 = ema_200.iloc[-1]
        
        # Trend scoring
        bullish_signals = 0
        bearish_signals = 0
        
        # RSI signals
        if latest_rsi > 50:
            bullish_signals += 1
        elif latest_rsi < 50:
            bearish_signals += 1
        
        # MACD signals
        if latest_macd > latest_signal and latest_histogram > 0:
            bullish_signals += 2
        elif latest_macd < latest_signal and latest_histogram < 0:
            bearish_signals += 2
        
        # ADX and DI signals
        if latest_adx > 25:  # Strong trend
            if latest_pos_di > latest_neg_di:
                bullish_signals += 2
            else:
                bearish_signals += 2
        
        # Supertrend signals
        if latest_st_direction > 0:
            bullish_signals += 2
        else:
            bearish_signals += 2
        
        # EMA signals
        if latest_close > latest_ema_20 > latest_ema_50:
            bullish_signals += 2
        elif latest_close < latest_ema_20 < latest_ema_50:
            bearish_signals += 2
        
        # Long-term trend
        if latest_close > latest_ema_200:
            bullish_signals += 1
        else:
            bearish_signals += 1
        
        # Determine overall trend
        total_signals = bullish_signals + bearish_signals
        if total_signals == 0:
            trend_direction = TrendDirection.NEUTRAL
            trend_strength = 0
        else:
            trend_strength = abs(bullish_signals - bearish_signals) / total_signals * 100
            
            if bullish_signals > bearish_signals:
                if trend_strength > 70:
                    trend_direction = TrendDirection.STRONG_BULLISH
                else:
                    trend_direction = TrendDirection.BULLISH
            elif bearish_signals > bullish_signals:
                if trend_strength > 70:
                    trend_direction = TrendDirection.STRONG_BEARISH
                else:
                    trend_direction = TrendDirection.BEARISH
            else:
                trend_direction = TrendDirection.NEUTRAL
        
        return {
            'trend_direction': trend_direction,
            'trend_strength': trend_strength,
            'bullish_signals': bullish_signals,
            'bearish_signals': bearish_signals,
            'rsi': latest_rsi,
            'macd': latest_macd,
            'signal': latest_signal,
            'adx': latest_adx,
            'pos_di': latest_pos_di,
            'neg_di': neg_di,
            'supertrend_direction': 'UP' if latest_st_direction > 0 else 'DOWN',
            'price_above_ema20': latest_close > latest_ema_20,
            'price_above_ema50': latest_close > latest_ema_50,
            'price_above_ema200': latest_close > latest_ema_200
        }
