import random

def _handle_ball_search(gs, hand, base_name):
    if "dusk" in base_name and any(k in base_name for k in {"ball"}):
        if gs.get("my_decklist"):
            pokemon_ids = [k for k, v in gs["my_decklist"].items() if str(v.get("card_type", "")).startswith("POKEMON")]
            if pokemon_ids:
                gs["my_hand"] = hand + [random.choice(pokemon_ids)]
                gs["my_deck_count"] = gs.get("my_deck_count", 60) - 1
        return True
    if "ultra" in base_name and any(k in base_name for k in {"ball"}):
        discards = []
        for _ in range(min(2, len(hand))):
            discards.append(hand.pop(0))
        gs["my_discard"] = gs.get("my_discard", []) + discards
        added = _pick_random_card(gs)
        gs["my_hand"] = hand + [added]
        gs["my_deck_count"] = gs.get("my_deck_count", 60) - 1
        return True
    if any(k in base_name for k in {"ball"}):
        added = _pick_random_card(gs)
        gs["my_hand"] = hand + [added]
        gs["my_deck_count"] = gs.get("my_deck_count", 60) - 1
        return True
    if "secret box" in base_name or "petrel" in base_name:
        keys = list(gs.get("my_decklist", {}).keys()) if gs.get("my_decklist") else []
        added1 = random.choice(keys) if keys else 1
        added2 = random.choice(keys) if keys else 2
        gs["my_hand"] = hand + [added1, added2]
        gs["my_deck_count"] = gs.get("my_deck_count", 60) - 2
        return True
    return False

def _pick_random_card(gs):
    import random
    if gs.get("my_deck"):
        return random.choice(gs["my_deck"])
    if gs.get("my_decklist"):
        return random.choice(list(gs["my_decklist"].keys()))
    return 1
