from typing import Dict, Any, List

def collect_targets(game_state: Dict[str, Any], registry) -> dict:
    opp_active = game_state.get("opponent_active_pokemon") or {}
    opp_bench = game_state.get("opponent_bench", [])
    targets = []

    if isinstance(opp_active, dict) and opp_active.get("id"):
        cid = opp_active.get("id")
        card = registry.get_full_skill(cid)
        name = getattr(card, "card_name", "") if card else str(opp_active.get("name", ""))
        is_two_prizer = any(tag in name.lower() for tag in (" ex", " v", "vstar", "vmax", "ex"))
        targets.append({
            "slot": "active",
            "id": cid,
            "name": name,
            "prize_yield": 2 if is_two_prizer else 1,
            "hp": game_state.get("opponent_active_hp", 100)
        })

    if isinstance(opp_bench, list):
        for idx, bp in enumerate(opp_bench):
            if isinstance(bp, dict) and bp.get("id"):
                cid = bp.get("id")
                card = registry.get_full_skill(cid)
                name = getattr(card, "card_name", "") if card else str(bp.get("name", ""))
                is_two_prizer = any(tag in name.lower() for tag in (" ex", " v", "vstar", "vmax", "ex"))
                targets.append({
                    "slot": f"bench_{idx}",
                    "id": cid,
                    "name": name,
                    "prize_yield": 2 if is_two_prizer else 1,
                    "hp": bp.get("hp", 100)
                })
    return targets

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
