import logging
from collections import Counter
from typing import Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class PrizeTracker:
    def __init__(self, deck: Optional[list] = None):
        self.initial_decklist: Dict[int, int] = {}
        self._deck_search_used = False
        self._prized_ids: Dict[int, int] = {}
        self._prize_map: List[str] = []
        if deck is not None:
            self.initial_decklist = dict(Counter(int(c) for c in deck))

    def record_initial_decklist(self, decklist: Union[Dict[int, int], list]):
        try:
            if isinstance(decklist, list):
                self.initial_decklist = dict(Counter(int(c) for c in decklist))
            else:
                self.initial_decklist = {int(k): int(v) for k, v in decklist.items()}
            logger.info(f"PrizeTracker: recorded initial decklist with {len(self.initial_decklist)} entries")
        except (ValueError, TypeError) as e:
            logger.error(f"PrizeTracker: invalid decklist input: {e}")
            self.initial_decklist = {}

    def on_deck_search(self, hand: List[str], discard: List[str], board: List[str],
                       deck_contents: List[str], deck_remaining: int) -> Dict[int, int]:
        try:
            if not self.initial_decklist:
                logger.warning("PrizeTracker.on_deck_search: no initial decklist recorded")
                return {}
            self._deck_search_used = True
            revealed_counts: Counter = Counter()
            for cid_str in hand + discard + board + deck_contents:
                try:
                    revealed_counts[int(cid_str)] += 1
                except (ValueError, TypeError):
                    continue
            prized = {}
            for cid, total in self.initial_decklist.items():
                remaining = total - revealed_counts.get(cid, 0)
                if remaining > 0:
                    prized[cid] = remaining
            self._prized_ids = prized
            logger.info(f"PrizeTracker: deduced {len(prized)} prized card types ({self.prizes_remaining()} total prizes)")
            return prized
        except Exception as e:
            logger.error(f"PrizeTracker.on_deck_search failed: {e}", exc_info=True)
            return {}

    def calculate_prized_probabilities(self, visible: List[int], prizes_remaining: int) -> Dict[int, float]:
        from agents.prize_probability import calculate_prized_probabilities as _calc
        return _calc(self.initial_decklist, visible, prizes_remaining)

    def get_prized_ids(self) -> Dict[int, int]:
        return dict(self._prized_ids)

    def is_card_prized(self, card_id: int) -> bool:
        return card_id in self._prized_ids

    def prizes_remaining(self) -> int:
        try:
            return sum(self._prized_ids.values())
        except Exception as e:
            logger.error(f"PrizeTracker.prizes_remaining failed: {e}")
            return 0

    def get_certainty_enrichment(self) -> dict:
        try:
            if self._deck_search_used and self._prized_ids:
                return {
                    "prized_card_ids": self.get_prized_ids(),
                    "prizes_remaining": self.prizes_remaining(),
                    "prize_certainty": 1.0,
                }
            return {}
        except Exception as e:
            logger.error(f"PrizeTracker.get_certainty_enrichment failed: {e}")
            return {}

    def plan_prize_take(self, active_damage: int, active_element: str,
                        opponent_bench_hp: Dict[str, int],
                        opponent_active_hp: int) -> Dict[str, any]:
        try:
            if not self._prized_ids:
                return {"target": "active", "reason": "unknown_prizes"}
            remain = self.prizes_remaining()
            if remain <= 2:
                return {"target": "active", "reason": "close_game", "priority": "finisher"}
            return {"target": "active", "reason": f"{remain}_prizes_remaining"}
        except Exception as e:
            logger.error(f"PrizeTracker.plan_prize_take failed: {e}", exc_info=True)
            return {"target": "active", "reason": "fallback"}


from agents.prize_mapping import PrizeMappingHeuristic
