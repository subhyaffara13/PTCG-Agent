import logging
logger = logging.getLogger(__name__)

def _plan_prize_take(prize_tracker) -> dict:
    try:
        if not prize_tracker._prized_ids:
            return {"target": "active", "reason": "unknown_prizes"}
        remain = prize_tracker.prizes_remaining()
        if remain <= 2:
            return {"target": "active", "reason": "close_game", "priority": "finisher"}
        return {"target": "active", "reason": f"{remain}_prizes_remaining"}
    except Exception as e:
        logger.error(f"PrizeTracker.plan_prize_take failed: {e}", exc_info=True)
        return {"target": "active", "reason": "fallback"}

def _get_certainty_enrichment(prize_tracker) -> dict:
    try:
        if prize_tracker._deck_search_used and prize_tracker._prized_ids:
            return {
                "prized_card_ids": prize_tracker.get_prized_ids(),
                "prizes_remaining": prize_tracker.prizes_remaining(),
                "prize_certainty": 1.0,
            }
        return {}
    except Exception as e:
        logger.error(f"PrizeTracker.get_certainty_enrichment failed: {e}")
        return {}
