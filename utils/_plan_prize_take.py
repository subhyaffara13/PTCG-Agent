
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

