"""
This module defines the ChallengeManager class and various market challenges.
"""

import random
from typing import Callable, List, Tuple

class Challenge:
    """Represents a market challenge with a name, description, and effect."""

    def __init__(self, name: str, description: str, effect: Callable[[float, float], Tuple[float, float]]):
        """
        Initialize a Challenge.

        Args:
            name (str): The name of the challenge.
            description (str): A brief description of the challenge.
            effect (Callable): A function that takes current price and volatility and returns new values.
        """
        self.name = name
        self.description = description
        self.effect = effect

class ChallengeManager:
    """Manages and applies market challenges."""

    def __init__(self):
        """Initialize the ChallengeManager with a set of predefined challenges."""
        self.challenges: List[Challenge] = [
            Challenge(
                "Volatility Spike",
                "Market volatility suddenly increases.",
                lambda p, v: (p, v * 2)
            ),
            Challenge(
                "Market Crash",
                "A sudden downturn causes prices to plummet.",
                lambda p, v: (p * 0.8, v * 1.5)
            ),
            Challenge(
                "Bull Run",
                "A surge of optimism drives prices up.",
                lambda p, v: (p * 1.2, v * 1.2)
            ),
            Challenge(
                "Calm Markets",
                "Volatility decreases as markets enter a calm period.",
                lambda p, v: (p, v * 0.5)
            ),
            Challenge(
                "Economic News",
                "Breaking economic news causes price fluctuation.",
                lambda p, v: (p * random.uniform(0.9, 1.1), v * random.uniform(0.8, 1.2))
            )
        ]

    def get_random_challenge(self) -> Challenge:
        """
        Select a random challenge from the available challenges.

        Returns:
            Challenge: A randomly selected challenge.
        """
        return random.choice(self.challenges)

    def apply_challenge(self, price: float, volatility: float) -> Tuple[float, float, Challenge]:
        """
        Apply a random challenge to the given market state.

        Args:
            price (float): The current market price.
            volatility (float): The current market volatility.

        Returns:
            Tuple[float, float, Challenge]: The new price, new volatility, and the applied challenge.
        """
        challenge = self.get_random_challenge()
        new_price, new_volatility = challenge.effect(price, volatility)
        return new_price, new_volatility, challenge