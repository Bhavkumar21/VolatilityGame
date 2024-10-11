"""
This module defines the Market class, which simulates a financial market
with price movements and volatility changes.
"""

import random
import math
from dataclasses import dataclass

@dataclass
class MarketState:
    """Represents the current state of the market."""
    price: float
    volatility: float

class Market:
    """Simulates a financial market with price movements and volatility changes."""

    def __init__(self, initial_price: float, initial_volatility: float):
        """
        Initialize the market with a starting price and volatility.

        Args:
            initial_price (float): The starting price of the asset.
            initial_volatility (float): The starting volatility of the asset.
        """
        self.state = MarketState(initial_price, initial_volatility)
        self.day = 0

    def update(self):
        """
        Update the market state for a new day.
        
        This method simulates daily price movement based on the current volatility.
        It uses a log-normal distribution to model price changes and includes
        safeguards against extreme price movements.
        """
        self.day += 1
        
        # Calculate daily return using a normal distribution
        daily_return = random.gauss(0, self.state.volatility)
        
        # Update price using the log-normal distribution, with bounds
        try:
            price_factor = math.exp(daily_return)
            # Limit the price change to prevent extreme movements
            price_factor = max(0.5, min(2.0, price_factor))
            self.state.price *= price_factor
        except OverflowError:
            # If we get an overflow, limit the price change
            if daily_return > 0:
                self.state.price *= 2.0
            else:
                self.state.price *= 0.5

        # Ensure the price doesn't go too close to zero
        self.state.price = max(0.01, self.state.price)

    def apply_challenge(self, price_factor: float, volatility_factor: float):
        """
        Apply a market challenge by adjusting price and volatility.

        Args:
            price_factor (float): Factor to multiply the current price by.
            volatility_factor (float): Factor to multiply the current volatility by.
        """
        self.state.price *= price_factor
        self.state.volatility *= volatility_factor
        
        # Ensure the price and volatility don't go too low
        self.state.price = max(0.01, self.state.price)
        self.state.volatility = max(0.001, self.state.volatility)

    def get_state(self) -> MarketState:
        """
        Get the current market state.

        Returns:
            MarketState: The current price and volatility.
        """
        return self.state

    def __str__(self):
        """Return a string representation of the current market state."""
        return f"Day {self.day}: Price = {self.state.price:.2f}, Volatility = {self.state.volatility:.4f}"