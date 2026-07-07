"""
cb_agents/belief_state.py

Defines the BeliefState class for probabilistic tracking of opponent's hidden zones.
"""

from dataclasses import dataclass, field
from typing import Dict

@dataclass
class BeliefState:
    """
    Represents the agent's probabilistic belief about the opponent's hidden zones.
    """
    hand_probabilities: Dict[int, float] = field(default_factory=dict)
    prize_probabilities: Dict[int, float] = field(default_factory=dict)
    deck_probabilities: Dict[int, float] = field(default_factory=dict)
    
    # Internal tracking for total counts
    deck_size: int = 60
    hand_size: int = 7
    prize_size: int = 6
    
    # Track the exact counts of cards known in specific zones
    known_in_hand: Dict[int, int] = field(default_factory=dict)
    known_in_deck: Dict[int, int] = field(default_factory=dict)
    known_in_discard: Dict[int, int] = field(default_factory=dict)
    known_in_play: Dict[int, int] = field(default_factory=dict)
