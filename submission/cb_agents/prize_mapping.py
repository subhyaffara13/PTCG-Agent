import logging
from typing import Dict, List
from cb_agents.prize_tracker import PrizeTracker

logger = logging.getLogger(__name__)

class PrizeMappingHeuristic:
    def __init__(self, prize_tracker: PrizeTracker):
        if not isinstance(prize_tracker, PrizeTracker):
            logger.warning("PrizeMappingHeuristic: expected PrizeTracker instance")
        self.tracker = prize_tracker

    def evaluate_target(self, my_active_hp: int, opponent_active_hp: int,
                        opponent_bench: List[str], my_bench: List[str],
                        my_prizes: int, opponent_prizes: int) -> str:
        try:
            total_prizes = self.tracker.prizes_remaining()
            if my_prizes <= 2 and opponent_prizes >= 4:
                logger.debug("PrizeMapping: aggro_ko (close game)")
                return "aggro_ko"
            if total_prizes >= 3 and len(opponent_bench) >= 2:
                logger.debug("PrizeMapping: spread_damage (multi-prize turns)")
                return "spread_damage"
            if opponent_active_hp <= my_active_hp:
                return "active_ko"
            return "setup_attacker"
        except Exception as e:
            logger.error(f"PrizeMappingHeuristic.evaluate_target failed: {e}", exc_info=True)
            return "active_ko"
