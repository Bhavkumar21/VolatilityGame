"""
This module defines the MarketMaker base class and various market making strategies.
"""

from abc import ABC, abstractmethod

class MarketMaker(ABC):
    """Abstract base class for market makers."""

    @abstractmethod
    def make_market(self, price: float, volatility: float) -> tuple[float, float]:
        """
        Generate bid and ask prices based on the current market state.

        Args:
            price (float): The current market price.
            volatility (float): The current market volatility.

        Returns:
            tuple[float, float]: A tuple containing the (bid, ask) prices.
        """
        pass

class SimpleMarketMaker(MarketMaker):
    """A simple market maker that sets a fixed spread based on volatility."""

    def __init__(self, spread_multiplier: float = 0.1):
        self.spread_multiplier = spread_multiplier

    def make_market(self, price: float, volatility: float) -> tuple[float, float]:
        spread = price * volatility * self.spread_multiplier
        bid = max(0.01, price - spread)
        ask = price + spread
        return bid, ask

def get_market_maker_class(class_name: str):
    """Dynamically import and return the specified MarketMaker class."""
    try:
        return globals()[class_name]
    except KeyError:
        print(f"Error: MarketMaker class '{class_name}' not found.")
        print("Using SimpleMarketMaker as fallback.")
        return SimpleMarketMaker