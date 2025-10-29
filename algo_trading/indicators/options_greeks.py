"""
Options Greeks Calculator
Calculates Delta, Gamma, Theta, Vega for options pricing and risk assessment
"""

import numpy as np
from scipy.stats import norm
from typing import Dict, List, Tuple
from datetime import datetime
import pandas as pd


class OptionsGreeks:
    """
    Calculate options Greeks for CE (Call) and PE (Put) options
    Uses Black-Scholes model for European options
    """
    
    @staticmethod
    def calculate_d1_d2(
        spot_price: float,
        strike_price: float,
        time_to_expiry: float,
        risk_free_rate: float,
        volatility: float
    ) -> Tuple[float, float]:
        """
        Calculate d1 and d2 for Black-Scholes model
        
        Args:
            spot_price: Current spot price
            strike_price: Option strike price
            time_to_expiry: Time to expiry in years
            risk_free_rate: Risk-free interest rate (annual)
            volatility: Implied volatility (annual)
            
        Returns:
            Tuple of (d1, d2)
        """
        d1 = (np.log(spot_price / strike_price) + 
              (risk_free_rate + 0.5 * volatility ** 2) * time_to_expiry) / \
             (volatility * np.sqrt(time_to_expiry))
        d2 = d1 - volatility * np.sqrt(time_to_expiry)
        
        return d1, d2
    
    @staticmethod
    def calculate_call_price(
        spot_price: float,
        strike_price: float,
        time_to_expiry: float,
        risk_free_rate: float,
        volatility: float
    ) -> float:
        """
        Calculate theoretical call option price using Black-Scholes
        
        Args:
            spot_price: Current spot price
            strike_price: Option strike price
            time_to_expiry: Time to expiry in years
            risk_free_rate: Risk-free interest rate (annual)
            volatility: Implied volatility (annual)
            
        Returns:
            Call option price
        """
        if time_to_expiry <= 0:
            return max(0, spot_price - strike_price)
        
        d1, d2 = OptionsGreeks.calculate_d1_d2(
            spot_price, strike_price, time_to_expiry, risk_free_rate, volatility
        )
        
        call_price = (spot_price * norm.cdf(d1) - 
                     strike_price * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2))
        
        return call_price
    
    @staticmethod
    def calculate_put_price(
        spot_price: float,
        strike_price: float,
        time_to_expiry: float,
        risk_free_rate: float,
        volatility: float
    ) -> float:
        """
        Calculate theoretical put option price using Black-Scholes
        
        Args:
            spot_price: Current spot price
            strike_price: Option strike price
            time_to_expiry: Time to expiry in years
            risk_free_rate: Risk-free interest rate (annual)
            volatility: Implied volatility (annual)
            
        Returns:
            Put option price
        """
        if time_to_expiry <= 0:
            return max(0, strike_price - spot_price)
        
        d1, d2 = OptionsGreeks.calculate_d1_d2(
            spot_price, strike_price, time_to_expiry, risk_free_rate, volatility
        )
        
        put_price = (strike_price * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2) - 
                    spot_price * norm.cdf(-d1))
        
        return put_price
    
    @staticmethod
    def calculate_delta(
        spot_price: float,
        strike_price: float,
        time_to_expiry: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str = 'call'
    ) -> float:
        """
        Calculate Delta (rate of change of option price with respect to spot price)
        
        Args:
            spot_price: Current spot price
            strike_price: Option strike price
            time_to_expiry: Time to expiry in years
            risk_free_rate: Risk-free interest rate (annual)
            volatility: Implied volatility (annual)
            option_type: 'call' or 'put'
            
        Returns:
            Delta value
        """
        if time_to_expiry <= 0:
            if option_type.lower() == 'call':
                return 1.0 if spot_price > strike_price else 0.0
            else:
                return -1.0 if spot_price < strike_price else 0.0
        
        d1, _ = OptionsGreeks.calculate_d1_d2(
            spot_price, strike_price, time_to_expiry, risk_free_rate, volatility
        )
        
        if option_type.lower() == 'call':
            return norm.cdf(d1)
        else:  # put
            return norm.cdf(d1) - 1
    
    @staticmethod
    def calculate_gamma(
        spot_price: float,
        strike_price: float,
        time_to_expiry: float,
        risk_free_rate: float,
        volatility: float
    ) -> float:
        """
        Calculate Gamma (rate of change of Delta with respect to spot price)
        
        Args:
            spot_price: Current spot price
            strike_price: Option strike price
            time_to_expiry: Time to expiry in years
            risk_free_rate: Risk-free interest rate (annual)
            volatility: Implied volatility (annual)
            
        Returns:
            Gamma value
        """
        if time_to_expiry <= 0:
            return 0.0
        
        d1, _ = OptionsGreeks.calculate_d1_d2(
            spot_price, strike_price, time_to_expiry, risk_free_rate, volatility
        )
        
        gamma = norm.pdf(d1) / (spot_price * volatility * np.sqrt(time_to_expiry))
        
        return gamma
    
    @staticmethod
    def calculate_theta(
        spot_price: float,
        strike_price: float,
        time_to_expiry: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str = 'call'
    ) -> float:
        """
        Calculate Theta (rate of change of option price with respect to time)
        
        Args:
            spot_price: Current spot price
            strike_price: Option strike price
            time_to_expiry: Time to expiry in years
            risk_free_rate: Risk-free interest rate (annual)
            volatility: Implied volatility (annual)
            option_type: 'call' or 'put'
            
        Returns:
            Theta value (per year, divide by 365 for daily theta)
        """
        if time_to_expiry <= 0:
            return 0.0
        
        d1, d2 = OptionsGreeks.calculate_d1_d2(
            spot_price, strike_price, time_to_expiry, risk_free_rate, volatility
        )
        
        term1 = -(spot_price * norm.pdf(d1) * volatility) / (2 * np.sqrt(time_to_expiry))
        
        if option_type.lower() == 'call':
            term2 = risk_free_rate * strike_price * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2)
            theta = term1 - term2
        else:  # put
            term2 = risk_free_rate * strike_price * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2)
            theta = term1 + term2
        
        return theta
    
    @staticmethod
    def calculate_vega(
        spot_price: float,
        strike_price: float,
        time_to_expiry: float,
        risk_free_rate: float,
        volatility: float
    ) -> float:
        """
        Calculate Vega (rate of change of option price with respect to volatility)
        
        Args:
            spot_price: Current spot price
            strike_price: Option strike price
            time_to_expiry: Time to expiry in years
            risk_free_rate: Risk-free interest rate (annual)
            volatility: Implied volatility (annual)
            
        Returns:
            Vega value (per 1% change in volatility)
        """
        if time_to_expiry <= 0:
            return 0.0
        
        d1, _ = OptionsGreeks.calculate_d1_d2(
            spot_price, strike_price, time_to_expiry, risk_free_rate, volatility
        )
        
        vega = spot_price * norm.pdf(d1) * np.sqrt(time_to_expiry)
        
        return vega / 100  # Per 1% change
    
    @staticmethod
    def calculate_all_greeks(
        spot_price: float,
        strike_price: float,
        time_to_expiry: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str = 'call'
    ) -> Dict[str, float]:
        """
        Calculate all Greeks for an option
        
        Args:
            spot_price: Current spot price
            strike_price: Option strike price
            time_to_expiry: Time to expiry in years
            risk_free_rate: Risk-free interest rate (annual)
            volatility: Implied volatility (annual)
            option_type: 'call' or 'put'
            
        Returns:
            Dictionary with all Greeks
        """
        if option_type.lower() == 'call':
            price = OptionsGreeks.calculate_call_price(
                spot_price, strike_price, time_to_expiry, risk_free_rate, volatility
            )
        else:
            price = OptionsGreeks.calculate_put_price(
                spot_price, strike_price, time_to_expiry, risk_free_rate, volatility
            )
        
        delta = OptionsGreeks.calculate_delta(
            spot_price, strike_price, time_to_expiry, risk_free_rate, volatility, option_type
        )
        gamma = OptionsGreeks.calculate_gamma(
            spot_price, strike_price, time_to_expiry, risk_free_rate, volatility
        )
        theta = OptionsGreeks.calculate_theta(
            spot_price, strike_price, time_to_expiry, risk_free_rate, volatility, option_type
        )
        vega = OptionsGreeks.calculate_vega(
            spot_price, strike_price, time_to_expiry, risk_free_rate, volatility
        )
        
        return {
            'price': price,
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega,
            'theta_daily': theta / 365  # Daily theta
        }
    
    @staticmethod
    def select_optimal_strike(
        spot_price: float,
        strikes: List[float],
        time_to_expiry: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str = 'call',
        risk_tolerance: str = 'moderate'
    ) -> Dict[str, any]:
        """
        Select optimal strike price based on Greeks for moderate risk
        
        Args:
            spot_price: Current spot price
            strikes: List of available strike prices
            time_to_expiry: Time to expiry in years
            risk_free_rate: Risk-free interest rate (annual)
            volatility: Implied volatility (annual)
            option_type: 'call' or 'put'
            risk_tolerance: 'low', 'moderate', or 'high'
            
        Returns:
            Dictionary with optimal strike and its Greeks
        """
        strikes_analysis = []
        
        for strike in strikes:
            greeks = OptionsGreeks.calculate_all_greeks(
                spot_price, strike, time_to_expiry, risk_free_rate, volatility, option_type
            )
            
            # Calculate risk score based on Greeks
            # Higher delta = higher directional exposure
            # Higher gamma = more delta sensitivity
            # Higher theta = more time decay (negative for buyers)
            # Higher vega = more volatility sensitivity
            
            delta_abs = abs(greeks['delta'])
            gamma_score = greeks['gamma'] * spot_price  # Normalized gamma
            theta_score = abs(greeks['theta_daily'])
            vega_score = greeks['vega']
            
            # Risk scoring
            if risk_tolerance == 'low':
                # Prefer lower delta (0.3-0.5), lower gamma, moderate theta
                risk_score = abs(delta_abs - 0.4) + gamma_score * 0.5 + theta_score * 0.3
            elif risk_tolerance == 'moderate':
                # Prefer moderate delta (0.4-0.6), balanced Greeks
                risk_score = abs(delta_abs - 0.5) + gamma_score * 0.3 + theta_score * 0.2
            else:  # high
                # Prefer higher delta (0.6-0.8), accept higher gamma
                risk_score = abs(delta_abs - 0.7) + gamma_score * 0.2 + theta_score * 0.1
            
            strikes_analysis.append({
                'strike': strike,
                'risk_score': risk_score,
                'greeks': greeks,
                'moneyness': 'ITM' if (option_type == 'call' and strike < spot_price) or 
                                      (option_type == 'put' and strike > spot_price) else
                            'OTM' if (option_type == 'call' and strike > spot_price) or 
                                      (option_type == 'put' and strike < spot_price) else 'ATM'
            })
        
        # Sort by risk score and select optimal
        strikes_analysis.sort(key=lambda x: x['risk_score'])
        optimal = strikes_analysis[0]
        
        return {
            'optimal_strike': optimal['strike'],
            'greeks': optimal['greeks'],
            'moneyness': optimal['moneyness'],
            'risk_score': optimal['risk_score'],
            'all_strikes': strikes_analysis[:5]  # Top 5 options
        }
