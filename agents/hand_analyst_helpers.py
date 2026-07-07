from __future__ import annotations
from typing import Any

def score_hand_helper(hand: list[str], scoring_db: dict[str, dict[str, Any]]) -> list[tuple[str, float]]:
    try:
        from agents.card_registry import CardRegistry
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

def mean_ev_helper(scored_cards: list[tuple[str, float]]) -> float:
    if not scored_cards:
        return 0.0
    return sum(ev for _, ev in scored_cards) / len(scored_cards)

def derive_profile_helper(hand_score: float, thresholds: list[tuple[float, str]]) -> str:
    for threshold, profile in thresholds:
        if hand_score >= threshold:
            return profile
    return "defensive"

def best_card_helper(scored_cards: list[tuple[str, float]]) -> str:
    if not scored_cards:
        return "(empty hand)"
    return max(scored_cards, key=lambda t: t[1])[0]
