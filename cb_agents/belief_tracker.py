import logging
from typing import Dict, List, Any
from cb_agents.belief_state import BeliefState
from cb_agents.belief_helpers import hypergeometric_prob, sample_determinization
from cb_agents.belief_tracker_recalc import recalculate_probabilities

logger = logging.getLogger(__name__)

class BeliefTracker:
    def __init__(self, initial_deck: Dict[int, int] = None):
        self.state = BeliefState()
        self.assumed_deck = initial_deck or {}
        self.locked_prize_ids: set = set()
        self.prize_guaranteed_counts: Dict[int, int] = {}
        self._prob_cache: Dict[str, float] = {}
        self._initialize_probabilities()

    def _initialize_probabilities(self):
        total_cards = sum(self.assumed_deck.values()) if self.assumed_deck else 60
        if total_cards == 0:
            return

        self.state.deck_size = total_cards - 7 - 6
        self.state.hand_size = 7
        self.state.prize_size = 6

        for card_id, count in self.assumed_deck.items():
            prob_in_deck = count / total_cards
            self.state.deck_probabilities[card_id] = prob_in_deck

            prob_in_hand = hypergeometric_prob(total_cards, count, 7)
            self.state.hand_probabilities[card_id] = prob_in_hand

            prob_in_prizes = hypergeometric_prob(total_cards, count, 6)
            self.state.prize_probabilities[card_id] = prob_in_prizes

    def update_on_play(self, card_id: int):
        card_id = int(card_id)
        self.state.hand_size = max(0, self.state.hand_size - 1)
        self.state.known_in_play[card_id] = self.state.known_in_play.get(card_id, 0) + 1
        if card_id in self.state.known_in_hand:
            self.state.known_in_hand[card_id] -= 1
            if self.state.known_in_hand[card_id] <= 0:
                del self.state.known_in_hand[card_id]
        self._recalculate_probabilities()

    def update_on_draw(self, n: int):
        self.state.deck_size = max(0, self.state.deck_size - n)
        self.state.hand_size += n
        self._recalculate_probabilities()

    def update_on_search(self, card_id: int):
        card_id = int(card_id)
        self.state.deck_size = max(0, self.state.deck_size - 1)
        self.state.hand_size += 1
        self.state.known_in_hand[card_id] = self.state.known_in_hand.get(card_id, 0) + 1
        self._recalculate_probabilities()

    def update_on_discard(self, card_id: int):
        card_id = int(card_id)
        self.state.hand_size = max(0, self.state.hand_size - 1)
        self.state.known_in_discard[card_id] = self.state.known_in_discard.get(card_id, 0) + 1
        self._recalculate_probabilities()

    def _recalculate_probabilities(self):
        recalculate_probabilities(self.state, self.assumed_deck, self.prize_guaranteed_counts)

    def lock_prizes(self, prized_ids: Dict[int, int], full_search: bool = True):
        self.locked_prize_ids.clear()
        self.prize_guaranteed_counts.clear()
        total_locked = 0
        for card_id in self.assumed_deck:
            count = prized_ids.get(card_id, 0)
            if count > 0:
                self.state.prize_probabilities[card_id] = 1.0
                self.locked_prize_ids.add(card_id)
                self.prize_guaranteed_counts[card_id] = count
                total_locked += count
            elif full_search:
                self.state.prize_probabilities[card_id] = 0.0
        logger.info(f"BeliefTracker: locked {total_locked} prized cards ({len(prized_ids)} types) at 100% certainty")

    def get_threat_score(self) -> float:
        score = 0.0
        for prob in self.state.hand_probabilities.values():
            score += prob
        return score

    def sample_determinization(self) -> Dict[str, List[int]]:
        return sample_determinization(self.state, self.assumed_deck, self.prize_guaranteed_counts)

    def probability_opponent_holds(self, card_name: str) -> float:
        key = card_name.lower().strip()
        if key in self._prob_cache:
            return self._prob_cache[key]
        from cb_agents.belief_tracker_opponent_holds import probability_opponent_holds_helper
        val = probability_opponent_holds_helper(
            card_name,
            self.assumed_deck,
            self.state.deck_size,
            self.state.hand_size,
            self.state.known_in_play,
            self.state.known_in_discard
        )
        self._prob_cache[key] = val
        return val
