"""
Unified Option Resolver & Utility Evaluator
Provides robust, name-resolved smart choice selection across both local simulation and Kaggle runtime.
"""

from typing import Any

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


def make_smart_choice_unified(select: dict, observation: dict, fallback_action: list, registry) -> list:
    """Evaluates option choices using utility scores, evolution predecessors, and smart discard inversion."""
    options = get_val(select, "option", [])
    if not options:
        return fallback_action

    max_count = get_val(select, "maxCount", 1)
    sel_type = get_val(select, "type")

    if not registry:
        return fallback_action

    current = get_val(observation, "current", {})
    my_idx = get_val(current, "yourIndex", 0)
    
    # Resolve names into all options
    resolve_option_names(options, observation, my_idx, registry)

    # Detect discard choice
    is_discard = False
    if sel_type in (1, 2, 4):
        if sel_type == 4 or str(get_val(select, "context", "")).lower() in ("discard", "energy_discard"):
            is_discard = True

    # Score options
    scored_options = []
    for idx, opt in enumerate(options):
        score = 0.0
        card_name = get_val(opt, "name", "")
        card_id = get_val(opt, "id")
        
        card = None
        if card_id is not None:
            card = registry.get_full_skill(card_id)
        if card is None and card_name:
            card = registry.get_full_skill(card_name)

        if card:
            score = getattr(card, "utility_score", 0.0)
            card_id_int = getattr(card, "card_id", None)
            if card_id_int is not None and hasattr(registry, "learned_dos"):
                if int(card_id_int) in registry.learned_dos:
                    score += 12.0
                if hasattr(registry, "learned_donts") and int(card_id_int) in registry.learned_donts:
                    score -= 12.0

        # Type-specific scoring
        opt_type = get_val(opt, "type")
        if opt_type in (12, 13):  # Attack
            score += 50.0
        elif opt_type in (8, 9) and "attach" in str(get_val(select, "context", "")).lower():  # Energy attach
            score += 20.0

        scored_options.append((idx, score))

    # Discard inversion: lowest scoring cards get picked for discard
    if is_discard:
        scored_options.sort(key=lambda x: x[1])
    else:
        scored_options.sort(key=lambda x: x[1], reverse=True)

    selected = [idx for idx, _ in scored_options[:max_count]]
    if len(selected) < max_count:
        for idx in range(len(options)):
            if idx not in selected:
                selected.append(idx)
                if len(selected) == max_count:
                    break
    return selected
