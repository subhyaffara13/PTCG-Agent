
def calculate_prized_probabilities(initial_decklist: Dict[int, int], visible: List[int], prizes_remaining: int) -> Dict[int, float]:
    try:
        total = sum(initial_decklist.values())
        visible_counts = Counter(visible)
        unseen_total = total - len(visible)
        if unseen_total < prizes_remaining or prizes_remaining <= 0:
            return {}
        probs = {}
        for cid, total_count in initial_decklist.items():
            visible_count = visible_counts.get(cid, 0)
            unseen = total_count - visible_count
            if unseen <= 0:
                probs[cid] = 0.0
            else:
                ways_total = math.comb(unseen_total, prizes_remaining)
                ways_avoid = math.comb(unseen_total - unseen, prizes_remaining)
                probs[cid] = round(1.0 - ways_avoid / ways_total, 2)
        return probs
    except Exception as e:
        logger.error(f"calculate_prized_probabilities failed: {e}", exc_info=True)
        return {}


def calculate_prized_probabilities(initial_decklist: Dict[int, int], visible: List[int], prizes_remaining: int) -> Dict[int, float]:
    try:
        total = sum(initial_decklist.values())
        visible_counts = Counter(visible)
        unseen_total = total - len(visible)
        if unseen_total < prizes_remaining or prizes_remaining <= 0:
            return {}
        probs = {}
        for cid, total_count in initial_decklist.items():
            visible_count = visible_counts.get(cid, 0)
            unseen = total_count - visible_count
            if unseen <= 0:
                probs[cid] = 0.0
            else:
                ways_total = math.comb(unseen_total, prizes_remaining)
                ways_avoid = math.comb(unseen_total - unseen, prizes_remaining)
                probs[cid] = round(1.0 - ways_avoid / ways_total, 2)
        return probs
    except Exception as e:
        logger.error(f"calculate_prized_probabilities failed: {e}", exc_info=True)
        return {}


def calculate_prized_probabilities(initial_decklist: Dict[int, int], visible: List[int], prizes_remaining: int) -> Dict[int, float]:
    try:
        total = sum(initial_decklist.values())
        visible_counts = Counter(visible)
        unseen_total = total - len(visible)
        if unseen_total <= 0 or prizes_remaining <= 0:
            return {}
        probs = {}
        for cid, total_count in initial_decklist.items():
            visible_count = visible_counts.get(cid, 0)
            unseen = total_count - visible_count
            if unseen <= 0:
                probs[cid] = 0.0
            else:
                ways_total = math.comb(unseen_total, prizes_remaining)
                ways_avoid = math.comb(unseen_total - unseen, prizes_remaining)
                probs[cid] = round(1.0 - ways_avoid / ways_total, 2)
        return probs
    except Exception as e:
        logger.error(f"calculate_prized_probabilities failed: {e}", exc_info=True)
        return {}

