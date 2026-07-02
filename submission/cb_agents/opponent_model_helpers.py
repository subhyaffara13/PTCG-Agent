"""
agents/opponent_model_helpers.py

Helper logic for OpponentModel: archetype classification and action predictions.
"""

from __future__ import annotations
from typing import Dict, List, Any


# Map Pokemon IDs to archetypes for fast lookup
KEY_ID_TO_ARCHETYPE = {
    "1092": "setup",
    "721": "aggro",
    "722": "aggro",
    "1145": "stall",
    "1163": "stall",
    "1121": "control",
    "1262": "combo"
}

def identify_opponent_archetype(revealed_state: List[Any], archetypes: Dict[str, Any]) -> tuple[str, float]:
    """Identifies archetype and returns (archetype_name, confidence)."""
    # 1. Fast ID check
    for card in revealed_state:
        if str(card) in KEY_ID_TO_ARCHETYPE:
            return KEY_ID_TO_ARCHETYPE[str(card)], 0.99
            
    total_revealed = len(revealed_state)
    if total_revealed < 3 or not archetypes:
        return "unknown", 0.0

    best_match_count = 0
    best_archetype = "unknown"
    
    for arch_name, arch_data in archetypes.items():
        signature_cards = set(arch_data.get("signature_cards", []))
        card_pool = set(arch_data.get("card_pool", []))
        
        matches = sum(1 for c in revealed_state if c in signature_cards or c in card_pool)
        if matches > best_match_count:
            best_match_count = matches
            best_archetype = arch_name
            
    if best_match_count > 0:
        return best_archetype, round(best_match_count / total_revealed, 4)
        
    return "unknown", 0.0

def predict_opponent_action(archetype: str, prizes_remaining: int, turn_number: int) -> str:
    """Predicts next opponent action based on archetype and state variables."""
    if archetype == "aggro":
        return "attack" if prizes_remaining < 6 else "attach_energy"
    elif archetype == "control":
        return "play_trainer_disruption" if prizes_remaining <= 3 else "stall"
    elif archetype == "combo":
        return "execute_combo" if turn_number >= 3 else "setup_bench"
    return "unknown"
