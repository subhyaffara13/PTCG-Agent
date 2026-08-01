
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

