from . import Any

def get_val(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    try:
        return getattr(obj, key, default)
    except Exception:
        return default

def resolve_option_names(options: list, observation: dict, my_idx: int, registry) -> None:
    """Dynamically resolves card names into option dictionaries based on hand/bench/active indices."""
    if not registry or not observation:
        return

    try:
        current = get_val(observation, "current", {})
        players = get_val(current, "players", [])
        if len(players) <= my_idx or not players[my_idx]:
            return

        my_state = players[my_idx]
        hand = get_val(my_state, "hand", [])

        for opt in options:
            if not isinstance(opt, dict):
                continue
            
            opt_type = opt.get("type")
            card_id = opt.get("id")
            
            # If coordinates are present (area=2 is hand, 4 is active, 5/12 is bench)
            if card_id is None:
                area = opt.get("area")
                idx = opt.get("index")
                p_idx = opt.get("playerIndex", my_idx)
                
                if p_idx == my_idx and area == 2 and idx is not None and 0 <= idx < len(hand):
                    card_item = hand[idx]
                    if isinstance(card_item, dict):
                        card_id = card_item.get("id")
                    elif isinstance(card_item, (int, str)):
                        card_id = card_item
                        
            if card_id is not None:
                card_entry = registry.get_full_skill(card_id)
                if card_entry and hasattr(card_entry, "card_name"):
                    opt["name"] = card_entry.card_name
                    opt["card_type"] = getattr(getattr(card_entry, "card_type", None), "name", "")
    except Exception:
        pass

