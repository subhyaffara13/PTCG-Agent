import logging
from typing import Dict, List, Any
from cb_agents.belief_state import BeliefState
from cb_agents.belief_helpers import hypergeometric_prob, sample_determinization

logger = logging.getLogger(__name__)

class BeliefTracker:
    """
    Tracks the opponent's hidden zones (hand, deck, prizes) probabilistically.
    """
    def __init__(self, initial_deck: Dict[int, int] = None):
        self.state = BeliefState()
        self.assumed_deck = initial_deck or {}
        self._initialize_probabilities()
        
    def _initialize_probabilities(self):
        """Sets up initial probability distributions based on assumed deck."""
        total_cards = sum(self.assumed_deck.values()) if self.assumed_deck else 60
        if total_cards == 0:
            return
            
        for card_id, count in self.assumed_deck.items():
            prob_in_deck = count / total_cards
            self.state.deck_probabilities[card_id] = prob_in_deck
            
            prob_in_hand = hypergeometric_prob(60, count, 7)
            self.state.hand_probabilities[card_id] = prob_in_hand
            
            prob_in_prizes = hypergeometric_prob(60, count, 6)
            self.state.prize_probabilities[card_id] = prob_in_prizes

    def update_on_play(self, card_id: int):
        """Opponent played a card from hand."""
        self.state.hand_size = max(0, self.state.hand_size - 1)
        self.state.known_in_play[card_id] = self.state.known_in_play.get(card_id, 0) + 1
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
                if self.state.known_in_hand.get(card_id, 0) > 0:
                    self.state.hand_probabilities[card_id] = 1.0
                else:
                    self.state.hand_probabilities[card_id] = hypergeometric_prob(cards_unseen, remaining, self.state.hand_size)
                
                self.state.deck_probabilities[card_id] = hypergeometric_prob(cards_unseen, remaining, self.state.deck_size)
                self.state.prize_probabilities[card_id] = hypergeometric_prob(cards_unseen, remaining, self.state.prize_size)
            else:
                self.state.hand_probabilities[card_id] = 0.0
                self.state.deck_probabilities[card_id] = 0.0
                self.state.prize_probabilities[card_id] = 0.0

    def get_threat_score(self) -> float:
        """Returns an estimated danger level based on likely hand contents."""
        score = 0.0
        for prob in self.state.hand_probabilities.values():
            score += prob
        return score

    def sample_determinization(self) -> Dict[str, List[int]]:
        """Samples a concrete imagined state of opponent's hidden zones."""
        return sample_determinization(self.state, self.assumed_deck)
