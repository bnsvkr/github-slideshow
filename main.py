"""
Main Application Entry Point
Runs the algorithmic trading system
"""

import logging
import sys
import time
from datetime import datetime
from typing import Optional

from algo_trading.core.fyers_client import FyersAPIClient
from algo_trading.strategies.options_strategy import OptionsStrategy
from algo_trading.utils.config import ConfigManager, Config


def setup_logging(config: Config) -> None:
    """
    Setup logging configuration
    
    Args:
        config: Configuration object
    """
    log_level = getattr(logging, config.logging.level.upper(), logging.INFO)
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # File handler
    if config.logging.log_file:
        file_handler = logging.FileHandler(config.logging.log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Console handler
    if config.logging.console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)


def is_trading_time(config: Config) -> bool:
    """
    Check if current time is within trading hours
    
    Args:
        config: Configuration object
        
    Returns:
        True if within trading hours
    """
    if not config.schedule.enabled:
        return True
    
    now = datetime.now()
    
    # Check trading day
    weekday = now.strftime('%a').upper()
    if weekday not in config.schedule.trading_days:
        return False
    
    # Check trading hours
    start_hour, start_min = map(int, config.schedule.start_time.split(':'))
    end_hour, end_min = map(int, config.schedule.end_time.split(':'))
    
    start_time = now.replace(hour=start_hour, minute=start_min, second=0, microsecond=0)
    end_time = now.replace(hour=end_hour, minute=end_min, second=0, microsecond=0)
    
    return start_time <= now <= end_time


def run_strategy_once(strategy: OptionsStrategy, logger: logging.Logger) -> None:
    """
    Run strategy once
    
    Args:
        strategy: Options strategy instance
        logger: Logger instance
    """
    try:
        logger.info("=" * 80)
        logger.info(f"Running strategy at {datetime.now()}")
        logger.info("=" * 80)
        
        results = strategy.run_strategy()
        
        # Log signals
        logger.info(f"Generated {len(results['signals'])} signals")
        for signal in results['signals']:
            if signal['signal'] != 'NO_SIGNAL':
                logger.info(f"Signal: {signal['signal']} for {signal['symbol']}")
                logger.info(f"  Trend: {signal['trend_direction']} (strength: {signal['trend_strength']:.2f})")
                if signal.get('strike_info'):
                    logger.info(f"  Optimal Strike: {signal['strike_info']['optimal_strike']}")
                    logger.info(f"  Greeks: {signal['strike_info']['greeks']}")
        
        # Log positions
        logger.info(f"Opened {len(results['positions'])} new positions")
        for position in results['positions']:
            if position['status'] == 'SUCCESS':
                logger.info(f"Position: {position['signal']} - {position['symbol']}")
                logger.info(f"  Strike: {position['strike']}, Entry: {position['entry_price']:.2f}")
        
        # Log errors
        if results['errors']:
            logger.error(f"Encountered {len(results['errors'])} errors")
            for error in results['errors']:
                logger.error(f"  {error}")
        
        logger.info("Strategy run completed")
        
    except Exception as e:
        logger.error(f"Error running strategy: {e}", exc_info=True)


def run_continuous(config: Config, strategy: OptionsStrategy, logger: logging.Logger) -> None:
    """
    Run strategy continuously based on schedule
    
    Args:
        config: Configuration object
        strategy: Options strategy instance
        logger: Logger instance
    """
    logger.info("Starting continuous trading mode")
    logger.info(f"Trading hours: {config.schedule.start_time} - {config.schedule.end_time}")
    logger.info(f"Check interval: {config.schedule.check_interval_minutes} minutes")
    logger.info(f"Trading days: {', '.join(config.schedule.trading_days)}")
    
    try:
        while True:
            if is_trading_time(config):
                run_strategy_once(strategy, logger)
                
                # Wait for next check interval
                wait_seconds = config.schedule.check_interval_minutes * 60
                logger.info(f"Waiting {config.schedule.check_interval_minutes} minutes for next check...")
                time.sleep(wait_seconds)
            else:
                now = datetime.now()
                logger.info(f"Outside trading hours at {now.strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info("Waiting 60 seconds...")
                time.sleep(60)
                
    except KeyboardInterrupt:
        logger.info("Trading stopped by user")
    except Exception as e:
        logger.error(f"Fatal error in continuous mode: {e}", exc_info=True)


def main():
    """
    Main entry point
    """
    print("=" * 80)
    print("NSE Options Trading System")
    print("Using Fyers API with World-Class Indicators and Greeks")
    print("=" * 80)
    print()
    
    # Load configuration
    try:
        config_manager = ConfigManager("config.json")
        config = config_manager.load_config()
    except FileNotFoundError:
        print("Configuration file not found. Creating example configuration...")
        config_manager = ConfigManager()
        config_manager.create_example_config("config.example.json")
        print("\nExample configuration created at 'config.example.json'")
        print("Please copy it to 'config.json' and update with your Fyers credentials.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)
    
    # Setup logging
    setup_logging(config)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting NSE Options Trading System")
    logger.info(f"Trading symbols: {', '.join(config.trading.symbols)}")
    logger.info(f"Risk tolerance: {config.trading.risk_tolerance}")
    
    # Initialize Fyers client
    try:
        fyers_client = FyersAPIClient(
            client_id=config.fyers.client_id,
            access_token=config.fyers.access_token,
            redirect_uri=config.fyers.redirect_uri
        )
        logger.info("Fyers API client initialized")
    except Exception as e:
        logger.error(f"Error initializing Fyers client: {e}")
        sys.exit(1)
    
    # Initialize strategy
    try:
        strategy = OptionsStrategy(
            fyers_client=fyers_client,
            symbols=config.trading.symbols,
            risk_free_rate=config.trading.risk_free_rate,
            volatility_default=config.trading.volatility_default,
            risk_tolerance=config.trading.risk_tolerance,
            initial_stop_loss_pct=config.trading.initial_stop_loss_pct,
            initial_target_pct=config.trading.initial_target_pct,
            trailing_stop_pct=config.trading.trailing_stop_pct
        )
        logger.info("Options strategy initialized")
    except Exception as e:
        logger.error(f"Error initializing strategy: {e}")
        sys.exit(1)
    
    # Run strategy
    try:
        if config.schedule.enabled:
            run_continuous(config, strategy, logger)
        else:
            logger.info("Running strategy once (schedule disabled)")
            run_strategy_once(strategy, logger)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
