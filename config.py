"""
Configuration parameters for the Volatility Market Making Game.
"""

# Market simulation parameters
INITIAL_PRICE = 100.0
INITIAL_VOLATILITY = 0.02
SIMULATION_DAYS = 63

# Challenge parameters
VOLATILITY_SPIKE_FACTOR = 2.0
MARKET_CRASH_FACTOR = 0.8
BULL_RUN_FACTOR = 1.2
CALM_MARKET_FACTOR = 0.5

# Market maker parameters
BASE_SPREAD = 0.01
SPREAD_MULTIPLIER = 2.0
INVENTORY_LIMIT = 100

# Scoring parameters
NEGATIVE_PNL_PENALTY = 10
CONSECUTIVE_POSITIVE_BONUS = 5

# Logging parameters
LOG_FILE = "market_making_game.log"

# Analysis parameters
RISK_FREE_RATE = 0.02
VOLATILITY_WINDOW = 30

# Order book simulation parameters
ORDER_BOOK_DEPTH = 5
MAX_SPREAD_PERCENTAGE = 0.01