from typing import Dict, List

def on_deck_search(prize_tracker, hand: List[str], discard: List[str], board: List[str],
                   deck_contents: List[str], deck_remaining: int) -> Dict[int, int]:
    try:
        if not prize_tracker.initial_decklist:
            logger.warning("PrizeTracker.on_deck_search: no initial decklist recorded")
            return {}
        prize_tracker._deck_search_used = True
        revealed_counts: Counter = Counter()
        for cid_str in hand + discard + board + deck_contents:
            try:
                revealed_counts[int(cid_str)] += 1
            except (ValueError, TypeError):
                continue
        prized = {}
        for cid, total in prize_tracker.initial_decklist.items():
            remaining = total - revealed_counts.get(cid, 0)
            if remaining > 0:
                prized[cid] = remaining
        prize_tracker._prized_ids = prized
        logger.info(f"PrizeTracker: deduced {len(prized)} prized card types ({prize_tracker.prizes_remaining()} total prizes)")
        return prized
    except Exception as e:
        logger.error(f"PrizeTracker.on_deck_search failed: {e}", exc_info=True)
        return {}


def on_deck_search(prize_tracker, hand: List[str], discard: List[str], board: List[str],
                   deck_contents: List[str], deck_remaining: int) -> Dict[int, int]:
    try:
        if not prize_tracker.initial_decklist:
            logger.warning("PrizeTracker.on_deck_search: no initial decklist recorded")
            return {}
        prize_tracker._deck_search_used = True
        revealed_counts: Counter = Counter()
        for cid_str in hand + discard + board + deck_contents:
            try:
                revealed_counts[int(cid_str)] += 1
            except (ValueError, TypeError):
                continue
        prized = {}
        for cid, total in prize_tracker.initial_decklist.items():
            remaining = total - revealed_counts.get(cid, 0)
            if remaining > 0:
                prized[cid] = remaining
        prize_tracker._prized_ids = prized
        logger.info(f"PrizeTracker: deduced {len(prized)} prized card types ({prize_tracker.prizes_remaining()} total prizes)")
        return prized
    except Exception as e:
        logger.error(f"PrizeTracker.on_deck_search failed: {e}", exc_info=True)
        return {}

