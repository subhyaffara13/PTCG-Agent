"""
agents/belief_helpers.py

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
    if N <= 0 or K <= 0 or n <= 0 or N < K or N < n:
        return 0.0
    
    try:
        prob_zero = math.comb(N - K, n) / math.comb(N, n)
        return 1.0 - prob_zero
    except ValueError:
        return 0.0

def sample_determinization(state: Any, assumed_deck: Dict[int, int]) -> Dict[str, List[int]]:
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
        unseen_pool.extend([card_id] * remaining)
        
        # Force cards we KNOW are in hand
        for _ in range(state.known_in_hand.get(card_id, 0)):
            sampled_hand.append(card_id)

    # Shuffle the unseen pool
    random.shuffle(unseen_pool)
    
    # Fill the rest of the hand
    needed_hand = max(0, state.hand_size - len(sampled_hand))
    sampled_hand.extend(unseen_pool[:needed_hand])
    unseen_pool = unseen_pool[needed_hand:]
    
    # Fill prizes
    needed_prizes = state.prize_size
    sampled_prizes.extend(unseen_pool[:needed_prizes])
    unseen_pool = unseen_pool[needed_prizes:]
    
    # The rest is the deck
    sampled_deck.extend(unseen_pool)
    
    return {
        "hand": sampled_hand,
        "prizes": sampled_prizes,
        "deck": sampled_deck
    }
