import math

def _compute_holds_probability(target_ids: list, assumed_deck: dict, deck_size: int,
                               hand_size: int, known_in_play: dict, known_in_discard: dict,
                               known_in_hand: dict | None, prize_size: int) -> float:
    N = deck_size + hand_size + max(0, prize_size)
    H = hand_size
    if N <= 0 or H <= 0:
        return 0.0
    D = 0
    for cid in target_ids:
        played = known_in_play.get(cid, 0) + known_in_discard.get(cid, 0) + (known_in_hand.get(cid, 0) if known_in_hand else 0)
        D += max(0, assumed_deck.get(cid, 0) - played)
    if D <= 0:
        return 0.0
    if N - D < H:
        return 1.0
    try:
        prob_none = math.comb(N - D, H) / math.comb(N, H)
        base_prob = 1.0 - prob_none
        if H >= 6:
            base_prob = min(1.0, base_prob * 1.15)
        return base_prob
    except (ValueError, ZeroDivisionError):
        return 0.0
