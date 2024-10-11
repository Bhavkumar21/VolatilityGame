"""
This module defines the Game class, which orchestrates the market making simulation.
"""

import logging
import random
from typing import List, Tuple
from dataclasses import dataclass

from market import Market
from challenges import ChallengeManager
from market_maker import MarketMaker

@dataclass
class TradeResult:
    """Represents the result of a single trade."""
    trade_type: str
    price: float
    quantity: int

class Game:
    def __init__(self, market: Market, challenge_manager: ChallengeManager, market_maker: MarketMaker, days: int):
        self.market = market
        self.challenge_manager = challenge_manager
        self.market_maker = market_maker
        self.days = days
        self.total_pnl = 0.0
        self.daily_results: List[Tuple[int, float, float, float, str]] = []

    def run(self) -> float:
        """Run the game simulation and return the final score."""
        logging.info("Starting game simulation")

        for day in range(1, self.days + 1):
            daily_pnl = self.simulate_day(day)
            self.total_pnl += daily_pnl
            logging.info(f"Day {day} completed. Daily PnL: {daily_pnl:.2f}, Total PnL: {self.total_pnl:.2f}")

        logging.info(f"Game ended. Total P&L: {self.total_pnl:.2f}")
        return self.calculate_score()

    def simulate_day(self, day: int) -> float:
        """Simulate a single trading day and return the daily P&L."""
        # Update market state
        self.market.update()

        # Apply random challenge
        new_price, new_volatility, challenge = self.challenge_manager.apply_challenge(
            self.market.get_state().price, 
            self.market.get_state().volatility
        )
        self.market.apply_challenge(new_price / self.market.get_state().price, new_volatility / self.market.get_state().volatility)

        # Get market maker quotes
        bid, ask = self.market_maker.make_market(self.market.get_state().price, self.market.get_state().volatility)

        # Simulate trades
        trades = self.simulate_trades(bid, ask)
        daily_pnl = self.calculate_daily_pnl(trades)

        # Log daily results
        self.log_daily_results(day, bid, ask, daily_pnl, challenge.name)

        return daily_pnl


    def simulate_trades(self, bid: float, ask: float) -> List[TradeResult]:
        """Simulate trades based on market maker quotes."""
        trades = []
        market_price = self.market.get_state().price
        
        # Widen the trading range slightly
        buffer = 0.001  # 0.1% buffer
        
        if market_price <= bid * (1 + buffer):
            trades.append(TradeResult("buy", bid, 1))
        elif market_price >= ask * (1 - buffer):
            trades.append(TradeResult("sell", ask, 1))
        
        # Add a small chance of random trading
        if random.random() < 0.1:  # 10% chance of random trade
            if random.choice([True, False]):
                trades.append(TradeResult("buy", bid, 1))
            else:
                trades.append(TradeResult("sell", ask, 1))
        
        # Log trade execution for debugging
        if trades:
            for trade in trades:
                logging.info(f"Trade executed: {trade.trade_type} at {trade.price}")
        else:
            logging.info(f"No trade executed. Market price: {market_price}, Bid: {bid}, Ask: {ask}")
        return trades

    def calculate_daily_pnl(self, trades: List[TradeResult]) -> float:
        """Calculate the daily P&L based on trades."""
        daily_pnl = 0.0
        market_price = self.market.get_state().price
        for trade in trades:
            if trade.trade_type == "buy":
                daily_pnl += market_price - trade.price
            else:  # sell
                daily_pnl += trade.price - market_price
        
        # Log P&L calculation for debugging
        logging.info(f"Daily P&L calculated: {daily_pnl}")
        
        return daily_pnl

    def log_daily_results(self, day: int, bid: float, ask: float, pnl: float, challenge: str):
        """Log the results of each trading day."""
        self.daily_results.append((day, bid, ask, pnl, challenge))
        logging.info(f"Day {day}: Bid={bid:.2f}, Ask={ask:.2f}, P&L={pnl:.2f}, Challenge={challenge}")

    def calculate_score(self) -> float:
        """Calculate the final score based on total P&L and other factors."""
        score = self.total_pnl

        # Penalty for negative P&L days
        negative_pnl_days = sum(1 for _, _, _, pnl, _ in self.daily_results if pnl < 0)
        score -= negative_pnl_days * 10

        # Bonus for consistent positive P&L
        consecutive_positive_days = self.get_max_consecutive_positive_days()
        score += consecutive_positive_days * 5

        logging.info(f"Score calculation: Total PnL: {self.total_pnl:.2f}, "
                     f"Negative PnL days: {negative_pnl_days}, "
                     f"Max consecutive positive days: {consecutive_positive_days}")

        return max(0, score)  # Ensure the score is non-negative

    def get_max_consecutive_positive_days(self) -> int:
        """Calculate the maximum streak of consecutive days with positive P&L."""
        max_streak = current_streak = 0
        for _, _, _, pnl, _ in self.daily_results:
            if pnl > 0:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        return max_streak