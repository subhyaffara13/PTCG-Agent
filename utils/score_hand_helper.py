from typing import Any

def score_hand_helper(hand: list[str], scoring_db: dict[str, dict[str, Any]]) -> list[tuple[str, float]]:
    try:
        from cb_agents.card_registry import CardRegistry
        registry = CardRegistry()
    except Exception:
        registry = None

    scored = []
    for card_name in hand:
        card_name_str = str(card_name)
        if card_name_str.isdigit() and registry:
            c = registry.get(int(card_name_str))
            if c and c.card_name:
                card_name_str = c.card_name
        entry = scoring_db.get(card_name_str.lower(), {})
        ev_score = float(entry.get("ev_score", 0.0))
        scored.append((card_name_str, ev_score))
    return scored


def score_hand_helper(hand: list[str], scoring_db: dict[str, dict[str, Any]]) -> list[tuple[str, float]]:
    try:
        from cb_agents.card_registry import CardRegistry
        registry = CardRegistry()
    except Exception:
        registry = None

    scored = []
    for card_name in hand:
        card_name_str = str(card_name)
        if card_name_str.isdigit() and registry:
            c = registry.get(int(card_name_str))
            if c and c.card_name:
                card_name_str = c.card_name
        entry = scoring_db.get(card_name_str.lower(), {})
        ev_score = float(entry.get("ev_score", 0.0))
        scored.append((card_name_str, ev_score))
    return scored


def score_hand_helper(hand: list[str], scoring_db: dict[str, dict[str, Any]]) -> list[tuple[str, float]]:
    try:
        from cb_agents.card_registry import CardRegistry
        registry = CardRegistry()
    except Exception:
        registry = None

    scored = []
    for card_name in hand:
        card_name_str = str(card_name)
        if card_name_str.isdigit() and registry:
            c = registry.get(int(card_name_str))
            if c and c.card_name:
                card_name_str = c.card_name
        entry = scoring_db.get(card_name_str.lower(), {})
        ev_score = float(entry.get("ev_score", 0.0))
        scored.append((card_name_str, ev_score))
    return scored

