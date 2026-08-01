from typing import Any, Dict, List
import random

def sample_determinization(state: Any, assumed_deck: Dict[int, int], prize_guaranteed_counts: Dict[int, int] = None) -> Dict[str, List[int]]:
    """
    Samples a concrete 'imagined' state of the opponent's hidden zones 
    based on the current belief state.
    """
    sampled_hand = []
    sampled_prizes = []
    sampled_deck = []
    
    hand_size = getattr(state, "hand_size", 0)
    prize_size = getattr(state, "prize_size", 0)
    deck_size = getattr(state, "deck_size", 0)

    if not assumed_deck:
        return {
            "hand": [0] * hand_size,
            "prizes": [0] * prize_size,
            "deck": [0] * deck_size
        }

    known_in_hand = getattr(state, "known_in_hand", {})
    known_in_play = getattr(state, "known_in_play", {})
    known_in_discard = getattr(state, "known_in_discard", {})
    prize_probabilities = getattr(state, "prize_probabilities", {})

    unseen_pool = []
    for card_id, total_count in assumed_deck.items():
        known = (known_in_hand.get(card_id, 0) + 
                 known_in_play.get(card_id, 0) + 
                 known_in_discard.get(card_id, 0))
        remaining = max(0, total_count - known)
        
        if prize_guaranteed_counts and int(card_id) in prize_guaranteed_counts:
            g_count = prize_guaranteed_counts[int(card_id)]
            for _ in range(g_count):
                if remaining > 0:
                    remaining -= 1
                    sampled_prizes.append(card_id)
        elif prize_probabilities:
            prob = prize_probabilities.get(int(card_id), 0.0)
            if prob >= 1.0:
                if remaining > 0:
                    remaining -= 1
                    sampled_prizes.append(card_id)
                    
        unseen_pool.extend([card_id] * remaining)
        
        for _ in range(known_in_hand.get(card_id, 0)):
            sampled_hand.append(card_id)

    random.shuffle(unseen_pool)

    needed_hand = max(0, hand_size - len(sampled_hand))
    sampled_hand.extend(unseen_pool[:needed_hand])
    unseen_pool = unseen_pool[needed_hand:]

    needed_prizes = max(0, prize_size - len(sampled_prizes))
    sampled_prizes.extend(unseen_pool[:needed_prizes])
    unseen_pool = unseen_pool[needed_prizes:]
    
    sampled_deck.extend(unseen_pool)
    
    return {
        "hand": sampled_hand,
        "prizes": sampled_prizes,
        "deck": sampled_deck
    }
