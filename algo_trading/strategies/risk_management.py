"""
Trailing Stop-Loss and Dynamic Target Management
Implements adaptive risk management strategies
"""

from typing import Dict, Optional, Tuple
from enum import Enum
import logging


class PositionDirection(Enum):
    """Position direction"""
    LONG = "LONG"
    SHORT = "SHORT"


class TrailingStopLoss:
    """
    Implements trailing stop-loss mechanism with dynamic target adjustment
    """
    
    def __init__(
        self,
        entry_price: float,
        direction: PositionDirection,
        initial_stop_loss_pct: float = 2.0,
        initial_target_pct: float = 5.0,
        trailing_stop_pct: float = 1.5,
        target_trail_increment_pct: float = 2.0
    ):
        """
        Initialize trailing stop-loss
        
        Args:
            entry_price: Entry price of the position
            direction: LONG or SHORT position
            initial_stop_loss_pct: Initial stop-loss percentage
            initial_target_pct: Initial target percentage
            trailing_stop_pct: Trailing stop percentage
            target_trail_increment_pct: Target increment percentage when moving up
        """
        self.entry_price = entry_price
        self.direction = direction
        self.initial_stop_loss_pct = initial_stop_loss_pct
        self.initial_target_pct = initial_target_pct
        self.trailing_stop_pct = trailing_stop_pct
        self.target_trail_increment_pct = target_trail_increment_pct
        
        # Calculate initial levels
        if direction == PositionDirection.LONG:
            self.stop_loss = entry_price * (1 - initial_stop_loss_pct / 100)
            self.target = entry_price * (1 + initial_target_pct / 100)
        else:  # SHORT
            self.stop_loss = entry_price * (1 + initial_stop_loss_pct / 100)
            self.target = entry_price * (1 - initial_target_pct / 100)
        
        self.highest_price = entry_price
        self.lowest_price = entry_price
        self.current_price = entry_price
        self.target_hit_count = 0
        
        self.logger = logging.getLogger(__name__)
    
    def update(self, current_price: float, trend_strength: float = 50.0) -> Dict[str, any]:
        """
        Update stop-loss and target based on current price and trend
        
        Args:
            current_price: Current market price
            trend_strength: Trend strength (0-100), higher = stronger trend
            
        Returns:
            Dictionary with updated levels and signals
        """
        self.current_price = current_price
        previous_stop_loss = self.stop_loss
        previous_target = self.target
        
        if self.direction == PositionDirection.LONG:
            # Update highest price
            if current_price > self.highest_price:
                self.highest_price = current_price
                
                # Trail stop-loss upward
                new_stop_loss = self.highest_price * (1 - self.trailing_stop_pct / 100)
                if new_stop_loss > self.stop_loss:
                    self.stop_loss = new_stop_loss
                    self.logger.info(f"Trailing stop-loss updated: {self.stop_loss:.2f}")
                
                # Check if target should be moved up based on trend strength
                if trend_strength > 60 and current_price >= self.target * 0.95:
                    # Strong uptrend, move target higher
                    self.target = current_price * (1 + self.target_trail_increment_pct / 100)
                    self.target_hit_count += 1
                    self.logger.info(f"Target moved up to: {self.target:.2f} (hit #{self.target_hit_count})")
            
            # Check for stop-loss hit
            stop_loss_hit = current_price <= self.stop_loss
            target_hit = current_price >= self.target
            
            # Calculate profit/loss percentage
            pnl_pct = ((current_price - self.entry_price) / self.entry_price) * 100
            
        else:  # SHORT position
            # Update lowest price
            if current_price < self.lowest_price:
                self.lowest_price = current_price
                
                # Trail stop-loss downward
                new_stop_loss = self.lowest_price * (1 + self.trailing_stop_pct / 100)
                if new_stop_loss < self.stop_loss:
                    self.stop_loss = new_stop_loss
                    self.logger.info(f"Trailing stop-loss updated: {self.stop_loss:.2f}")
                
                # Check if target should be moved down based on trend strength
                if trend_strength > 60 and current_price <= self.target * 1.05:
                    # Strong downtrend, move target lower
                    self.target = current_price * (1 - self.target_trail_increment_pct / 100)
                    self.target_hit_count += 1
                    self.logger.info(f"Target moved down to: {self.target:.2f} (hit #{self.target_hit_count})")
            
            # Check for stop-loss hit
            stop_loss_hit = current_price >= self.stop_loss
            target_hit = current_price <= self.target
            
            # Calculate profit/loss percentage
            pnl_pct = ((self.entry_price - current_price) / self.entry_price) * 100
        
        return {
            'current_price': current_price,
            'entry_price': self.entry_price,
            'stop_loss': self.stop_loss,
            'target': self.target,
            'stop_loss_updated': self.stop_loss != previous_stop_loss,
            'target_updated': self.target != previous_target,
            'stop_loss_hit': stop_loss_hit,
            'target_hit': target_hit,
            'pnl_pct': pnl_pct,
            'highest_price': self.highest_price if self.direction == PositionDirection.LONG else None,
            'lowest_price': self.lowest_price if self.direction == PositionDirection.SHORT else None,
            'target_hit_count': self.target_hit_count
        }
    
    def get_current_levels(self) -> Dict[str, float]:
        """
        Get current stop-loss and target levels
        
        Returns:
            Dictionary with current levels
        """
        return {
            'entry_price': self.entry_price,
            'current_price': self.current_price,
            'stop_loss': self.stop_loss,
            'target': self.target,
            'direction': self.direction.value
        }
    
    def should_exit(self, current_price: float, trend_strength: float = 50.0) -> Tuple[bool, str]:
        """
        Determine if position should be exited
        
        Args:
            current_price: Current market price
            trend_strength: Trend strength (0-100)
            
        Returns:
            Tuple of (should_exit, reason)
        """
        update_result = self.update(current_price, trend_strength)
        
        if update_result['stop_loss_hit']:
            return True, "Stop-loss hit"
        
        if update_result['target_hit']:
            # Check if trend is still strong
            if trend_strength < 40:
                return True, "Target hit and trend weakening"
            else:
                # Keep position open and trail target
                return False, "Target hit but trend still strong, trailing target"
        
        return False, "Position active"


class PositionManager:
    """
    Manages multiple positions with trailing stop-loss and targets
    """
    
    def __init__(self):
        """Initialize position manager"""
        self.positions: Dict[str, TrailingStopLoss] = {}
        self.logger = logging.getLogger(__name__)
    
    def add_position(
        self,
        symbol: str,
        entry_price: float,
        direction: PositionDirection,
        initial_stop_loss_pct: float = 2.0,
        initial_target_pct: float = 5.0,
        trailing_stop_pct: float = 1.5,
        target_trail_increment_pct: float = 2.0
    ) -> TrailingStopLoss:
        """
        Add a new position
        
        Args:
            symbol: Trading symbol
            entry_price: Entry price
            direction: Position direction
            initial_stop_loss_pct: Initial stop-loss percentage
            initial_target_pct: Initial target percentage
            trailing_stop_pct: Trailing stop percentage
            target_trail_increment_pct: Target increment percentage
            
        Returns:
            TrailingStopLoss instance
        """
        position = TrailingStopLoss(
            entry_price=entry_price,
            direction=direction,
            initial_stop_loss_pct=initial_stop_loss_pct,
            initial_target_pct=initial_target_pct,
            trailing_stop_pct=trailing_stop_pct,
            target_trail_increment_pct=target_trail_increment_pct
        )
        
        self.positions[symbol] = position
        self.logger.info(f"Added position for {symbol} at {entry_price}")
        
        return position
    
    def update_position(
        self,
        symbol: str,
        current_price: float,
        trend_strength: float = 50.0
    ) -> Optional[Dict[str, any]]:
        """
        Update a position
        
        Args:
            symbol: Trading symbol
            current_price: Current market price
            trend_strength: Trend strength
            
        Returns:
            Update result or None if position not found
        """
        if symbol not in self.positions:
            self.logger.warning(f"Position not found for {symbol}")
            return None
        
        return self.positions[symbol].update(current_price, trend_strength)
    
    def remove_position(self, symbol: str) -> bool:
        """
        Remove a position
        
        Args:
            symbol: Trading symbol
            
        Returns:
            True if position was removed, False otherwise
        """
        if symbol in self.positions:
            del self.positions[symbol]
            self.logger.info(f"Removed position for {symbol}")
            return True
        
        return False
    
    def get_position(self, symbol: str) -> Optional[TrailingStopLoss]:
        """
        Get a position
        
        Args:
            symbol: Trading symbol
            
        Returns:
            TrailingStopLoss instance or None
        """
        return self.positions.get(symbol)
    
    def get_all_positions(self) -> Dict[str, TrailingStopLoss]:
        """
        Get all positions
        
        Returns:
            Dictionary of all positions
        """
        return self.positions.copy()
