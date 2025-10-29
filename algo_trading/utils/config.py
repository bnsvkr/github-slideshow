"""
Configuration Management
Handles loading and validation of trading configuration
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
import logging


@dataclass
class FyersConfig:
    """Fyers API configuration"""
    client_id: str
    access_token: str
    redirect_uri: str = ""


@dataclass
class TradingConfig:
    """Trading strategy configuration"""
    symbols: List[str] = field(default_factory=lambda: ['NSE:NIFTY50-INDEX'])
    risk_free_rate: float = 0.065  # 6.5% annual
    volatility_default: float = 0.20  # 20% annual
    risk_tolerance: str = 'moderate'  # low, moderate, high
    initial_stop_loss_pct: float = 2.0
    initial_target_pct: float = 5.0
    trailing_stop_pct: float = 1.5
    target_trail_increment_pct: float = 2.0
    max_positions: int = 5
    position_size: int = 1  # Number of lots
    time_to_expiry_days: int = 7  # Preferred expiry


@dataclass
class ScheduleConfig:
    """Trading schedule configuration"""
    enabled: bool = False
    start_time: str = "09:20"  # Market opens at 9:15
    end_time: str = "15:20"  # Market closes at 3:30
    check_interval_minutes: int = 5
    trading_days: List[str] = field(default_factory=lambda: ['MON', 'TUE', 'WED', 'THU', 'FRI'])


@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    log_file: str = "trading.log"
    console_output: bool = True


@dataclass
class Config:
    """Main configuration"""
    fyers: FyersConfig
    trading: TradingConfig = field(default_factory=TradingConfig)
    schedule: ScheduleConfig = field(default_factory=ScheduleConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


class ConfigManager:
    """
    Configuration manager for the trading system
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize configuration manager
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
    
    def load_config(self) -> Config:
        """
        Load configuration from file
        
        Returns:
            Config object
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)
            
            # Parse Fyers config
            fyers_config = FyersConfig(**config_data.get('fyers', {}))
            
            # Parse Trading config
            trading_data = config_data.get('trading', {})
            trading_config = TradingConfig(**trading_data)
            
            # Parse Schedule config
            schedule_data = config_data.get('schedule', {})
            schedule_config = ScheduleConfig(**schedule_data)
            
            # Parse Logging config
            logging_data = config_data.get('logging', {})
            logging_config = LoggingConfig(**logging_data)
            
            config = Config(
                fyers=fyers_config,
                trading=trading_config,
                schedule=schedule_config,
                logging=logging_config
            )
            
            self.validate_config(config)
            return config
            
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise
    
    def validate_config(self, config: Config) -> None:
        """
        Validate configuration
        
        Args:
            config: Configuration to validate
        """
        # Validate Fyers config
        if not config.fyers.client_id:
            raise ValueError("Fyers client_id is required")
        if not config.fyers.access_token:
            raise ValueError("Fyers access_token is required")
        
        # Validate Trading config
        if not config.trading.symbols:
            raise ValueError("At least one trading symbol is required")
        
        if config.trading.risk_tolerance not in ['low', 'moderate', 'high']:
            raise ValueError("Risk tolerance must be 'low', 'moderate', or 'high'")
        
        if config.trading.initial_stop_loss_pct <= 0:
            raise ValueError("Initial stop loss percentage must be positive")
        
        if config.trading.initial_target_pct <= 0:
            raise ValueError("Initial target percentage must be positive")
        
        # Validate Schedule config
        if config.schedule.enabled:
            # Validate time format
            try:
                start_hour, start_min = map(int, config.schedule.start_time.split(':'))
                end_hour, end_min = map(int, config.schedule.end_time.split(':'))
                
                if not (0 <= start_hour < 24 and 0 <= start_min < 60):
                    raise ValueError("Invalid start time")
                if not (0 <= end_hour < 24 and 0 <= end_min < 60):
                    raise ValueError("Invalid end time")
            except:
                raise ValueError("Time format must be HH:MM")
        
        self.logger.info("Configuration validated successfully")
    
    def save_config(self, config: Config) -> None:
        """
        Save configuration to file
        
        Args:
            config: Configuration to save
        """
        try:
            config_dict = {
                'fyers': asdict(config.fyers),
                'trading': asdict(config.trading),
                'schedule': asdict(config.schedule),
                'logging': asdict(config.logging)
            }
            
            with open(self.config_path, 'w') as f:
                json.dump(config_dict, f, indent=2)
            
            self.logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            raise
    
    def create_example_config(self, output_path: str = "config.example.json") -> None:
        """
        Create an example configuration file
        
        Args:
            output_path: Path for example config file
        """
        example_config = Config(
            fyers=FyersConfig(
                client_id="YOUR_CLIENT_ID",
                access_token="YOUR_ACCESS_TOKEN",
                redirect_uri="https://your-redirect-uri.com"
            ),
            trading=TradingConfig(
                symbols=[
                    'NSE:NIFTY50-INDEX',
                    'NSE:BANKNIFTY-INDEX',
                    'NSE:SBIN-EQ',
                    'NSE:RELIANCE-EQ',
                    'NSE:TCS-EQ'
                ],
                risk_free_rate=0.065,
                volatility_default=0.20,
                risk_tolerance='moderate',
                initial_stop_loss_pct=2.0,
                initial_target_pct=5.0,
                trailing_stop_pct=1.5,
                target_trail_increment_pct=2.0,
                max_positions=5,
                position_size=1,
                time_to_expiry_days=7
            ),
            schedule=ScheduleConfig(
                enabled=True,
                start_time="09:20",
                end_time="15:20",
                check_interval_minutes=5,
                trading_days=['MON', 'TUE', 'WED', 'THU', 'FRI']
            ),
            logging=LoggingConfig(
                level="INFO",
                log_file="trading.log",
                console_output=True
            )
        )
        
        config_dict = {
            'fyers': asdict(example_config.fyers),
            'trading': asdict(example_config.trading),
            'schedule': asdict(example_config.schedule),
            'logging': asdict(example_config.logging)
        }
        
        with open(output_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
        
        print(f"Example configuration created at {output_path}")
