"""
agents/prize_tracker.py
Calculates prized card probabilities using hypergeometric math.
"""
import math
from collections import Counter

class PrizeTracker:
    def __init__(self, full_deck_list: list):
        self.full_deck = full_deck_list

    def calculate_prized_probabilities(self, visible_cards: list, prizes_remaining: int) -> dict:
        """
        visible_cards: list of card IDs currently visible (hand + board + discard).
        prizes_remaining: number of prizes remaining (1 to 6).
        Returns a dict mapping card_id to probability of it being in the prize cards.
        """
        deck_counts = Counter(self.full_deck)
        visible_counts = Counter(visible_cards)
        
        unseen_total = len(self.full_deck) - len(visible_cards)
        if unseen_total <= 0 or prizes_remaining <= 0:
            return {k: 0.0 for k in deck_counts}
            
        probabilities = {}
        for card_id, starting_count in deck_counts.items():
            visible_count = visible_counts.get(card_id, 0)
            hidden_count = max(0, starting_count - visible_count)
            
            if hidden_count == 0:
                probabilities[card_id] = 0.0
            else:
                try:
                    ways_to_avoid = math.comb(unseen_total - hidden_count, prizes_remaining)
                    total_ways = math.comb(unseen_total, prizes_remaining)
                    prob_avoid = ways_to_avoid / total_ways
                    probabilities[card_id] = max(0.0, min(1.0, 1.0 - prob_avoid))
                except Exception:
                    probabilities[card_id] = 0.0
                    
        return probabilities
