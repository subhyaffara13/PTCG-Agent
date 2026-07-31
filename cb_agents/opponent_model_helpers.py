"""
cb_agents/opponent_model_helpers.py

Helper logic for OpponentModel: archetype classification and action predictions.
"""

from __future__ import annotations
from typing import Dict, List, Any


# Map known competitive Pokemon IDs to archetypes for fast lookup
KEY_ID_TO_ARCHETYPE = {
    "721": "aggro",
    "722": "aggro",
    "979": "aggro",
    "1145": "stall",
    "1163": "stall",
    "1121": "control",
    "1262": "combo",
    "1260": "combo",
}

from cb_agents.card_registry import CardRegistry
_registry = None

def get_card_identifier(card_id: Any) -> str:
    global _registry
    if _registry is None:
        _registry = CardRegistry()
    entry = _registry.get(card_id)
    if entry:
        return entry.card_name.lower().replace(" ", "-")
    return str(card_id).lower()

def identify_opponent_archetype(revealed_state: List[Any], archetypes: Dict[str, Any]) -> tuple[str, float]:
    """Identifies archetype and returns (archetype_name, confidence)."""
    # 1. Fast ID check
    for card in revealed_state:
        if str(card) in KEY_ID_TO_ARCHETYPE:
            return KEY_ID_TO_ARCHETYPE[str(card)], 0.99
            
    total_revealed = len(revealed_state)
    if total_revealed < 1 or not archetypes:
        return "unknown", 0.0

    # Pre-compute card identifiers for all revealed cards once
    revealed_idents = [(str(c).lower().replace(" ", "-"), get_card_identifier(c)) for c in revealed_state]

    best_score = 0.0
    best_archetype = "unknown"
    has_sig_match = False
    
    for arch_name, arch_data in archetypes.items():
        signature_cards = [sig.lower().replace(" ", "-") for sig in arch_data.get("signature_cards", [])]
        card_pool = [cp.lower().replace(" ", "-") for cp in arch_data.get("card_pool", [])]
        
        score = 0.0
        arch_has_sig = False
        for raw_str, ident in revealed_idents:
            is_sig = (raw_str in signature_cards) or any((len(ident) > 4 and (ident in sig or sig in ident)) for sig in signature_cards)
            if is_sig:
                score += 2.0
                arch_has_sig = True
                continue
            is_pool = (raw_str in card_pool) or any((len(ident) > 4 and (ident in cp or cp in ident)) for cp in card_pool)
            if is_pool:
                score += 1.0
                
        if score > best_score:
            best_score = score
            best_archetype = arch_name
            has_sig_match = arch_has_sig
            
    if best_score > 0.0:
        if has_sig_match:
            confidence = min(0.95, 0.80 + (best_score * 0.05))
        else:
            confidence = round(best_score / (total_revealed * 2.0), 4) if total_revealed >= 3 else 0.0
        return best_archetype, confidence
        
    return "unknown", 0.0

def predict_opponent_action(archetype: str, prizes_remaining: int, turn_number: int) -> str:
    """Predicts next opponent action based on archetype and state variables."""
    if archetype == "aggro":
        return "attack" if prizes_remaining < 6 else "attach_energy"
    elif archetype == "control":
        return "play_trainer_disruption" if prizes_remaining <= 3 else "setup"
    elif archetype == "combo":
        return "execute_combo" if turn_number >= 3 else "setup_bench"
    return "unknown"
