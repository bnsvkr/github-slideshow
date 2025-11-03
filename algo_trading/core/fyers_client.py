"""
Fyers API Integration Module
Handles authentication, data fetching, and order placement
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import requests
import json


class FyersAPIClient:
    """
    Client for interacting with Fyers API
    Handles authentication, market data, and order management
    """
    
    def __init__(self, client_id: str, access_token: str, redirect_uri: str = None):
        """
        Initialize Fyers API client
        
        Args:
            client_id: Fyers application client ID
            access_token: Access token for authentication
            redirect_uri: Redirect URI for OAuth (optional)
        """
        self.client_id = client_id
        self.access_token = access_token
        self.redirect_uri = redirect_uri
        self.base_url = "https://api.fyers.in/api/v2"
        self.logger = logging.getLogger(__name__)
        
        # Set up headers
        self.headers = {
            'Authorization': f'{client_id}:{access_token}',
            'Content-Type': 'application/json'
        }
    
    def get_quotes(self, symbols: List[str]) -> Dict[str, Any]:
        """
        Get current market quotes for symbols
        
        Args:
            symbols: List of symbols (e.g., ['NSE:SBIN-EQ', 'NSE:NIFTY50-INDEX'])
            
        Returns:
            Dictionary with quote data
        """
        try:
            url = f"{self.base_url}/quotes"
            data = {'symbols': ','.join(symbols)}
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error fetching quotes: {e}")
            return {}
    
    def get_historical_data(
        self, 
        symbol: str, 
        resolution: str = "D",
        start_date: datetime = None,
        end_date: datetime = None,
        cont_flag: str = "1"
    ) -> Dict[str, Any]:
        """
        Get historical market data
        
        Args:
            symbol: Symbol to fetch (e.g., 'NSE:SBIN-EQ')
            resolution: Time resolution (1, 2, 3, 5, 10, 15, 30, 60, D, W, M)
            start_date: Start date for historical data
            end_date: End date for historical data
            cont_flag: Continuation flag (1 for continuous data)
            
        Returns:
            Dictionary with historical data
        """
        try:
            if start_date is None:
                start_date = datetime.now() - timedelta(days=365)
            if end_date is None:
                end_date = datetime.now()
            
            url = f"{self.base_url}/history"
            params = {
                'symbol': symbol,
                'resolution': resolution,
                'date_format': '1',
                'range_from': int(start_date.timestamp()),
                'range_to': int(end_date.timestamp()),
                'cont_flag': cont_flag
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error fetching historical data: {e}")
            return {}
    
    def get_option_chain(self, symbol: str, expiry: str = None) -> Dict[str, Any]:
        """
        Get option chain data for a symbol
        
        Args:
            symbol: Underlying symbol (e.g., 'NIFTY50')
            expiry: Expiry date (format: YYMMDD) - optional
            
        Returns:
            Dictionary with option chain data
        """
        try:
            url = f"{self.base_url}/optionchain"
            params = {
                'symbol': f'NSE:{symbol}-INDEX',
            }
            if expiry:
                params['expiry'] = expiry
                
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error fetching option chain: {e}")
            return {}
    
    def place_order(
        self,
        symbol: str,
        side: int,  # 1 for buy, -1 for sell
        qty: int,
        order_type: int = 2,  # 1: Limit, 2: Market, 3: Stop, 4: Stop Limit
        product_type: str = "INTRADAY",  # INTRADAY, CNC, MARGIN
        limit_price: float = 0,
        stop_price: float = 0,
        validity: str = "DAY",
        offline_order: bool = False,
        stop_loss: float = 0,
        take_profit: float = 0
    ) -> Dict[str, Any]:
        """
        Place an order
        
        Args:
            symbol: Trading symbol
            side: 1 for buy, -1 for sell
            qty: Quantity to trade
            order_type: Type of order (1-4)
            product_type: Product type (INTRADAY, CNC, MARGIN)
            limit_price: Limit price for limit orders
            stop_price: Stop price for stop orders
            validity: Order validity (DAY, IOC)
            offline_order: Whether order is offline
            stop_loss: Stop loss price
            take_profit: Take profit price
            
        Returns:
            Dictionary with order response
        """
        try:
            url = f"{self.base_url}/orders"
            order_data = {
                'symbol': symbol,
                'qty': qty,
                'type': order_type,
                'side': side,
                'productType': product_type,
                'validity': validity,
                'offlineOrder': offline_order,
            }
            
            if limit_price > 0:
                order_data['limitPrice'] = limit_price
            if stop_price > 0:
                order_data['stopPrice'] = stop_price
            if stop_loss > 0:
                order_data['stopLoss'] = stop_loss
            if take_profit > 0:
                order_data['takeProfit'] = take_profit
            
            response = requests.post(url, headers=self.headers, json=order_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error placing order: {e}")
            return {'s': 'error', 'message': str(e)}
    
    def modify_order(
        self,
        order_id: str,
        qty: int = None,
        order_type: int = None,
        limit_price: float = None,
        stop_price: float = None
    ) -> Dict[str, Any]:
        """
        Modify an existing order
        
        Args:
            order_id: Order ID to modify
            qty: New quantity
            order_type: New order type
            limit_price: New limit price
            stop_price: New stop price
            
        Returns:
            Dictionary with modification response
        """
        try:
            url = f"{self.base_url}/orders"
            modify_data = {'id': order_id}
            
            if qty is not None:
                modify_data['qty'] = qty
            if order_type is not None:
                modify_data['type'] = order_type
            if limit_price is not None:
                modify_data['limitPrice'] = limit_price
            if stop_price is not None:
                modify_data['stopPrice'] = stop_price
            
            response = requests.put(url, headers=self.headers, json=modify_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error modifying order: {e}")
            return {'s': 'error', 'message': str(e)}
    
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Cancel an order
        
        Args:
            order_id: Order ID to cancel
            
        Returns:
            Dictionary with cancellation response
        """
        try:
            url = f"{self.base_url}/orders"
            response = requests.delete(
                url,
                headers=self.headers,
                json={'id': order_id}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error canceling order: {e}")
            return {'s': 'error', 'message': str(e)}
    
    def get_positions(self) -> Dict[str, Any]:
        """
        Get current positions
        
        Returns:
            Dictionary with positions data
        """
        try:
            url = f"{self.base_url}/positions"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error fetching positions: {e}")
            return {}
    
    def get_orders(self) -> Dict[str, Any]:
        """
        Get all orders
        
        Returns:
            Dictionary with orders data
        """
        try:
            url = f"{self.base_url}/orders"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error fetching orders: {e}")
            return {}
    
    def get_funds(self) -> Dict[str, Any]:
        """
        Get account funds information
        
        Returns:
            Dictionary with funds data
        """
        try:
            url = f"{self.base_url}/funds"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error fetching funds: {e}")
            return {}
