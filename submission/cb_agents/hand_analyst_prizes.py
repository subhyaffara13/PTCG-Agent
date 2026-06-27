import math
from typing import Dict, List, Any

class HandPrizesMixin:
    def evaluate_prizes(
        self, hand: List[str], discard: List[str], board: List[str],
        deck_base_list: Dict[int, int], deck_remaining: int,
        has_searched_deck: bool = False
    ) -> tuple[int, int, Dict[str, float]]:
        revealed_counts = {}
        for cid in hand + discard + board:
            try:
                cid_int = int(cid)
                revealed_counts[cid_int] = revealed_counts.get(cid_int, 0) + 1
            except:
                pass

        total_revealed_count = sum(revealed_counts.values())
        total_starting_count = sum(deck_base_list.values()) if deck_base_list else 60
        total_unrevealed = max(0, total_starting_count - total_revealed_count)
        prize_remaining = max(0, total_unrevealed - deck_remaining)

        prized_probabilities = {}
        if has_searched_deck:
            return prize_remaining, total_unrevealed, prized_probabilities

        if total_unrevealed > 0 and prize_remaining > 0:
            def nCr(n, r):
                if r < 0 or r > n:
                    return 0
                return math.comb(n, r)

            for cid_int, start_count in deck_base_list.items():
                rev_count = revealed_counts.get(cid_int, 0)
                n_unrevealed = max(0, start_count - rev_count)
                if n_unrevealed > 0:
                    prob = 1.0 - (nCr(total_unrevealed - n_unrevealed, prize_remaining) / nCr(total_unrevealed, prize_remaining))
                    prized_probabilities[str(cid_int)] = round(prob, 4)
                else:
                    prized_probabilities[str(cid_int)] = 0.0

        return prize_remaining, total_unrevealed, prized_probabilities
