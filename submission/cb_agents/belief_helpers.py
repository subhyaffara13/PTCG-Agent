"""
cb_agents/belief_helpers.py

Helper functions for belief tracking: hypergeometric probabilities and state determinization.
"""

import math
import random
from typing import Dict, List, Any

def hypergeometric_prob(N: int, K: int, n: int) -> float:
    """
    Probability of exactly 1 success in n draws from N total with K successes.
    Returns the probability of drawing AT LEAST ONE.
    """
    if N <= 0 or K <= 0 or n <= 0 or N < K:
        return 0.0
    if N <= n:
        return 1.0
    
    try:
        prob_zero = math.comb(N - K, n) / math.comb(N, n)
        return 1.0 - prob_zero
    except ValueError:
        if N - K < n:
            return 1.0
        return 0.0

def sample_determinization(state: Any, assumed_deck: Dict[int, int], prize_guaranteed_counts: Dict[int, int] = None) -> Dict[str, List[int]]:
    """
    Samples a concrete 'imagined' state of the opponent's hidden zones 
    based on the current belief state.
    """
    sampled_hand = []
    sampled_prizes = []
    sampled_deck = []
    
    if not assumed_deck:
        return {
            "hand": [0] * state.hand_size,
            "prizes": [0] * state.prize_size,
            "deck": [0] * state.deck_size
        }

    # Build a pool of all unseen cards
    unseen_pool = []
    for card_id, total_count in assumed_deck.items():
        known = (state.known_in_hand.get(card_id, 0) + 
                 state.known_in_play.get(card_id, 0) + 
                 state.known_in_discard.get(card_id, 0))
        remaining = max(0, total_count - known)
        
        # Lock guaranteed prizes
        if prize_guaranteed_counts and card_id in prize_guaranteed_counts:
            g_count = prize_guaranteed_counts[card_id]
            for _ in range(g_count):
                if remaining > 0:
                    remaining -= 1
                    sampled_prizes.append(card_id)
        elif hasattr(state, 'prize_probabilities') and state.prize_probabilities:
            prob = state.prize_probabilities.get(str(card_id), 0.0)
            if prob >= 1.0:
                if remaining > 0:
                    remaining -= 1
                    sampled_prizes.append(card_id)
                    
        unseen_pool.extend([card_id] * remaining)
        
        # Force cards we KNOW are in hand
        for _ in range(state.known_in_hand.get(card_id, 0)):
            sampled_hand.append(card_id)

    # Fill the rest of the hand
    needed_hand = max(0, state.hand_size - len(sampled_hand))
    sampled_hand.extend(unseen_pool[:needed_hand])
    unseen_pool = unseen_pool[needed_hand:]

    # Fill remaining prizes
    needed_prizes = max(0, state.prize_size - len(sampled_prizes))
    sampled_prizes.extend(unseen_pool[:needed_prizes])
    unseen_pool = unseen_pool[needed_prizes:]
    
    # The rest is the deck
    sampled_deck.extend(unseen_pool)
    
    return {
        "hand": sampled_hand,
        "prizes": sampled_prizes,
        "deck": sampled_deck
    }
