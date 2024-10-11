# Volatility Market Making Game

## Introduction

Welcome to the Volatility Market Making Game! This educational simulation is designed for those who have just learned about market making and want to gain hands-on experience in a risk-free environment. By playing this game, you'll deepen your understanding of market making strategies, volatility impacts, and risk management in financial markets.

## What is Market Making?

Market making is a crucial function in financial markets where a trader (the market maker) continuously quotes both buy and sell prices for a financial instrument. The goal is to provide liquidity to the market and profit from the bid-ask spread while managing risk.

## Game Overview

In this simulation:
- You'll act as a market maker for 63 trading days (one quarter).
- Each day presents new market conditions and challenges.
- Your task is to set bid and ask prices based on the current market price and volatility.
- The game simulates trades based on your quotes and calculates your profit/loss.
- Various market events (like volatility spikes or market crashes) will test your strategy's resilience.

## How to Play

1. Clone this repository:
   ```
   git clone git@github.com:Bhavkumar21/VolatilityGame.git
   cd VolatilityGame
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the game:
   ```
   python main.py --market-maker SimpleMarketMaker
   ```

4. After the simulation, review your performance in the generated log file.

## Learning Objectives

By playing this game, you'll learn:
1. How to set bid-ask spreads based on market volatility.
2. The impact of market events on pricing strategies.
3. Risk management in volatile markets.
4. The balance between providing liquidity and managing inventory.
5. How different market making strategies perform under various conditions.

## Customizing Your Strategy

The game comes with a `SimpleMarketMaker` strategy. As you become more comfortable, try creating your own strategy:

1. Open `market_maker.py`
2. Create a new class that inherits from `MarketMaker`
3. Implement the `make_market` method with your custom logic
4. Run the game with your new strategy:
   ```
   python main.py --market-maker YourStrategyName
   ```

## Analyzing Your Performance

After each game, review the `market_making_game.log` file. Look for:
- Days with high profits or losses
- How your strategy performed during different market events
- Patterns in the market price and your quoted prices

## Tips for Improvement

1. Start with wider spreads and narrow them as you gain confidence.
2. Pay attention to the volatility and adjust your spreads accordingly.
3. Try to identify patterns in the market challenges and adapt your strategy.
4. Experiment with different approaches to handle extreme market events.

## Contributing

Found a bug or have an idea for improvement? Feel free to open an issue or submit a pull request!

## Disclaimer

This game is for educational purposes only and does not represent real market conditions. Always consult with financial professionals before engaging in actual market making or trading activities.

Happy market making, and may your spreads be ever in your favor :)
