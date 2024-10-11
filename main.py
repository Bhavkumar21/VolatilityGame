"""
Main entry point for the Volatility Market Making Game.
This script sets up the game environment, initializes components, and runs the simulation.
"""

import argparse
import logging
from datetime import datetime
import time

from market import Market
from challenges import ChallengeManager
from market_maker import get_market_maker_class
from game import Game
from config import INITIAL_PRICE, INITIAL_VOLATILITY, SIMULATION_DAYS, LOG_FILE

def setup_logging():
    """Configure logging for the game."""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Volatility Market Making Game")
    parser.add_argument(
        "--market-maker",
        type=str,
        default="SimpleMarketMaker",
        help="Name of the MarketMaker class to use"
    )
    return parser.parse_args()

def main():
    """Main function to run the Volatility Market Making Game."""
    # Set up logging and parse arguments
    setup_logging()
    args = parse_arguments()

    logging.info("Starting Volatility Market Making Game")
    
    # Initialize game components
    market = Market(INITIAL_PRICE, INITIAL_VOLATILITY)
    challenge_manager = ChallengeManager()
    
    MarketMakerClass = get_market_maker_class(args.market_maker)
    market_maker = MarketMakerClass()
    
    game = Game(market, challenge_manager, market_maker, SIMULATION_DAYS)

    # Run the game
    start_time = datetime.now()
    final_score = game.run()
    end_time = datetime.now()

    # Log and display results
    duration = (end_time - start_time).total_seconds()
    logging.info(f"Game completed in {duration:.2f} seconds")
    logging.info(f"Final Score: {final_score}")

    print(f"\nGame completed in {duration:.2f} seconds")
    print(f"Final Score: {final_score}")
    print(f"Check {LOG_FILE} for detailed game logs")

if __name__ == "__main__":
    main()