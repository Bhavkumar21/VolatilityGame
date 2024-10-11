# utils.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Tuple

def calculate_returns(prices: List[float]) -> List[float]:
    """
    Calculate the logarithmic returns of a price series.
    
    Args:
        prices (List[float]): List of prices.
    
    Returns:
        List[float]: List of logarithmic returns.
    """
    return [np.log(prices[i] / prices[i-1]) for i in range(1, len(prices))]

def calculate_volatility(returns: List[float], window: int = 30) -> List[float]:
    """
    Calculate rolling volatility of returns.
    
    Args:
        returns (List[float]): List of returns.
        window (int): Rolling window size.
    
    Returns:
        List[float]: List of volatilities.
    """
    return [np.std(returns[max(0, i-window):i]) * np.sqrt(252) for i in range(1, len(returns)+1)]

def sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """
    Calculate the Sharpe ratio of a strategy.
    
    Args:
        returns (List[float]): List of strategy returns.
        risk_free_rate (float): Annual risk-free rate.
    
    Returns:
        float: Sharpe ratio.
    """
    excess_returns = [r - risk_free_rate/252 for r in returns]
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)

def max_drawdown(pnl: List[float]) -> float:
    """
    Calculate the maximum drawdown of a PnL curve.
    
    Args:
        pnl (List[float]): List of cumulative PnL values.
    
    Returns:
        float: Maximum drawdown as a percentage.
    """
    peak = pnl[0]
    max_dd = 0
    for value in pnl:
        if value > peak:
            peak = value
        dd = (peak - value) / peak
        if dd > max_dd:
            max_dd = dd
    return max_dd

def plot_pnl_curve(days: List[int], pnl: List[float], title: str = "Cumulative PnL"):
    """
    Plot the cumulative PnL curve.
    
    Args:
        days (List[int]): List of trading days.
        pnl (List[float]): List of cumulative PnL values.
        title (str): Title of the plot.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(days, pnl)
    plt.title(title)
    plt.xlabel("Trading Day")
    plt.ylabel("Cumulative PnL")
    plt.grid(True)
    plt.show()

def calculate_bid_ask_spread(bid: float, ask: float) -> float:
    """
    Calculate the bid-ask spread as a percentage of the mid price.
    
    Args:
        bid (float): Bid price.
        ask (float): Ask price.
    
    Returns:
        float: Bid-ask spread as a percentage.
    """
    mid_price = (bid + ask) / 2
    return (ask - bid) / mid_price

def calculate_market_impact(trade_price: float, market_price: float) -> float:
    """
    Calculate the market impact of a trade.
    
    Args:
        trade_price (float): Price at which the trade was executed.
        market_price (float): Current market price.
    
    Returns:
        float: Market impact as a percentage.
    """
    return (trade_price - market_price) / market_price

def analyze_market_making_performance(daily_results: List[Tuple[int, float, float, float, str]]):
    """
    Analyze and print various performance metrics for a market making strategy.
    
    Args:
        daily_results (List[Tuple[int, float, float, float, str]]): 
            List of daily results (day, bid, ask, pnl, challenge).
    """
    df = pd.DataFrame(daily_results, columns=['Day', 'Bid', 'Ask', 'PnL', 'Challenge'])
    
    total_pnl = df['PnL'].sum()
    avg_daily_pnl = df['PnL'].mean()
    pnl_std = df['PnL'].std()
    
    sharpe = sharpe_ratio(df['PnL'].tolist())
    max_dd = max_drawdown(df['PnL'].cumsum().tolist())
    
    avg_spread = df.apply(lambda row: calculate_bid_ask_spread(row['Bid'], row['Ask']), axis=1).mean()
    
    print(f"Total PnL: ${total_pnl:.2f}")
    print(f"Average Daily PnL: ${avg_daily_pnl:.2f}")
    print(f"PnL Standard Deviation: ${pnl_std:.2f}")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Maximum Drawdown: {max_dd:.2%}")
    print(f"Average Bid-Ask Spread: {avg_spread:.2%}")
    
    print("\nPnL by Challenge Type:")
    print(df.groupby('Challenge')['PnL'].agg(['sum', 'mean', 'std']))
    
    plot_pnl_curve(df['Day'].tolist(), df['PnL'].cumsum().tolist())

def simulate_order_book(mid_price: float, depth: int = 5, max_spread: float = 0.01):
    """
    Simulate a simple order book.
    
    Args:
        mid_price (float): The mid price of the asset.
        depth (int): The number of levels to generate on each side.
        max_spread (float): The maximum spread as a percentage of mid price.
    
    Returns:
        Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]: Bids and asks as (price, quantity) tuples.
    """
    bids = [(mid_price * (1 - max_spread * (i+1)/depth), np.random.randint(1, 100)) for i in range(depth)]
    asks = [(mid_price * (1 + max_spread * (i+1)/depth), np.random.randint(1, 100)) for i in range(depth)]
    return bids, asks

def plot_order_book(bids: List[Tuple[float, float]], asks: List[Tuple[float, float]]):
    """
    Plot a simulated order book.
    
    Args:
        bids (List[Tuple[float, float]]): List of (price, quantity) tuples for bids.
        asks (List[Tuple[float, float]]): List of (price, quantity) tuples for asks.
    """
    bid_prices, bid_quantities = zip(*bids)
    ask_prices, ask_quantities = zip(*asks)
    
    plt.figure(figsize=(12, 6))
    plt.bar(bid_prices, bid_quantities, color='g', alpha=0.5, label='Bids')
    plt.bar(ask_prices, ask_quantities, color='r', alpha=0.5, label='Asks')
    plt.xlabel('Price')
    plt.ylabel('Quantity')
    plt.title('Simulated Order Book')
    plt.legend()
    plt.grid(True)
    plt.show()
