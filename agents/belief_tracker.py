import math
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

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

class BeliefTracker:
    """
    Tracks the opponent's hidden zones (hand, deck, prizes) probabilistically.
    
    As the opponent takes public actions (drawing, searching, discarding, playing cards),
    this module updates hypergeometric probability distributions to infer what cards the
    opponent is holding. This allows the StrategyAgent to anticipate threats and setups.
    """
    def __init__(self, initial_deck: Dict[int, int] = None):
        """
        Initializes the tracker with a generic deck distribution if exact opponent deck isn't known.
        If initial_deck is provided, it's a dict mapping card_id -> count in deck.
        """
        self.state = BeliefState()
        
        # If no specific deck is known, we could initialize with a generic prior
        # But for exact hypergeometric calcs we need counts. Let's assume an empty tracker 
        # until the opponent model predicts an archetype deck
        self.assumed_deck = initial_deck or {}
        self._initialize_probabilities()
        
    def _initialize_probabilities(self):
        """Sets up initial probability distributions based on assumed deck."""
        total_cards = sum(self.assumed_deck.values()) if self.assumed_deck else 60
        if total_cards == 0:
            return
            
        for card_id, count in self.assumed_deck.items():
            # Initial probabilities before drawing opening hand/prizes
            prob_in_deck = count / total_cards
            self.state.deck_probabilities[card_id] = prob_in_deck
            
            # Simple approximation for initial hand/prizes
            # True calculation uses hypergeometric dist
            prob_in_hand = self._hypergeometric_prob(60, count, 7)
            self.state.hand_probabilities[card_id] = prob_in_hand
            
            prob_in_prizes = self._hypergeometric_prob(60, count, 6)
            self.state.prize_probabilities[card_id] = prob_in_prizes

    def _hypergeometric_prob(self, N: int, K: int, n: int) -> float:
        """
        Probability of exactly 1 success in n draws from N total with K successes.
        (Simplified: we often just care about the expected value or probability of >0)
        Using expected value: E[X] = n * (K/N)
        We'll return the probability of drawing AT LEAST ONE.
        P(X >= 1) = 1 - P(X = 0)
        """
        if N <= 0 or K <= 0 or n <= 0 or N < K or N < n:
            return 0.0
        
        try:
            prob_zero = math.comb(N - K, n) / math.comb(N, n)
            return 1.0 - prob_zero
        except ValueError:
            return 0.0

    def update_on_play(self, card_id: int):
        """Opponent played a card from hand."""
        self.state.hand_size = max(0, self.state.hand_size - 1)
        # We now know this card is in play
        self.state.known_in_play[card_id] = self.state.known_in_play.get(card_id, 0) + 1
        # It's no longer in hand (at least one copy)
        self._recalculate_probabilities()

    def update_on_draw(self, n: int):
        """Opponent drew n cards."""
        self.state.deck_size = max(0, self.state.deck_size - n)
        self.state.hand_size += n
        self._recalculate_probabilities()

    def update_on_search(self, card_id: int):
        """Opponent searched deck for a specific card."""
        self.state.deck_size = max(0, self.state.deck_size - 1)
        self.state.hand_size += 1
        # We know exactly what entered their hand
        self.state.known_in_hand[card_id] = self.state.known_in_hand.get(card_id, 0) + 1
        self._recalculate_probabilities()

    def update_on_discard(self, card_id: int):
        """Card moved to discard."""
        self.state.known_in_discard[card_id] = self.state.known_in_discard.get(card_id, 0) + 1
        self._recalculate_probabilities()

    def _recalculate_probabilities(self):
        """Recomputes all probabilities based on known information."""
        if not self.assumed_deck:
            return
            
        cards_unseen = self.state.deck_size + self.state.prize_size + self.state.hand_size
        
        for card_id, total_count in self.assumed_deck.items():
            known = (self.state.known_in_hand.get(card_id, 0) + 
                     self.state.known_in_play.get(card_id, 0) + 
                     self.state.known_in_discard.get(card_id, 0))
                     
            remaining = max(0, total_count - known)
            
            if cards_unseen > 0:
                # If we know it's in hand, prob is 1.0. Otherwise use hypergeometric
                if self.state.known_in_hand.get(card_id, 0) > 0:
                    self.state.hand_probabilities[card_id] = 1.0
                else:
                    self.state.hand_probabilities[card_id] = self._hypergeometric_prob(cards_unseen, remaining, self.state.hand_size)
                
                self.state.deck_probabilities[card_id] = self._hypergeometric_prob(cards_unseen, remaining, self.state.deck_size)
                self.state.prize_probabilities[card_id] = self._hypergeometric_prob(cards_unseen, remaining, self.state.prize_size)
            else:
                self.state.hand_probabilities[card_id] = 0.0
                self.state.deck_probabilities[card_id] = 0.0
                self.state.prize_probabilities[card_id] = 0.0

    def get_threat_score(self) -> float:
        """Returns an estimated danger level based on likely hand contents."""
        # A true implementation would weight high-damage/combo cards
        score = 0.0
        for prob in self.state.hand_probabilities.values():
            score += prob
        return score
