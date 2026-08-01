
def compute_optimal_path(my_prizes_remaining: int, targets: list) -> dict:
    two_prizers = [t for t in targets if t["prize_yield"] == 2]
    one_prizers = [t for t in targets if t["prize_yield"] == 1]
    preferred_target_slot = None
    boss_boost = 0.0

    if my_prizes_remaining <= 2 and two_prizers:
        target = two_prizers[0]
        preferred_target_slot = target["slot"]
        boss_boost = 25.0
    elif my_prizes_remaining <= 4 and len(two_prizers) >= 2:
        benched_two = [t for t in two_prizers if t["slot"] != "active"]
        if benched_two:
            preferred_target_slot = benched_two[0]["slot"]
            boss_boost = 18.0

    return {
        "my_prizes_remaining": my_prizes_remaining,
        "two_prizer_count": len(two_prizers),
        "one_prizer_count": len(one_prizers),
        "preferred_target_slot": preferred_target_slot,
        "boss_priority_boost": boss_boost
    }


def compute_optimal_path(my_prizes_remaining: int, targets: list) -> dict:
    two_prizers = [t for t in targets if t["prize_yield"] == 2]
    one_prizers = [t for t in targets if t["prize_yield"] == 1]
    preferred_target_slot = None
    boss_boost = 0.0

    if my_prizes_remaining <= 2 and two_prizers:
        target = two_prizers[0]
        preferred_target_slot = target["slot"]
        boss_boost = 25.0
    elif my_prizes_remaining <= 4 and len(two_prizers) >= 2:
        benched_two = [t for t in two_prizers if t["slot"] != "active"]
        if benched_two:
            preferred_target_slot = benched_two[0]["slot"]
            boss_boost = 18.0

    return {
        "my_prizes_remaining": my_prizes_remaining,
        "two_prizer_count": len(two_prizers),
        "one_prizer_count": len(one_prizers),
        "preferred_target_slot": preferred_target_slot,
        "boss_priority_boost": boss_boost
    }

