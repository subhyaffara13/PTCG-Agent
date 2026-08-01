
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

