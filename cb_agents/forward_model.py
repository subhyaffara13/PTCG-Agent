import copy
import logging
from typing import Any

logger = logging.getLogger(__name__)

from cb_agents.forward_model_resolve import _resolve_base
from cb_agents.forward_model_gen import _regenerate_legal_actions, _check_win_conditions


def fast_clone_state(gs: dict) -> dict:
    clone = dict(gs)
    # Hand, discards, and decks
    for k in ["my_hand", "my_discard", "opponent_discard", "my_deck", "opponent_deck", "legal_actions"]:
        if k in clone and isinstance(clone[k], list):
            clone[k] = list(clone[k])
            
    # Active Pokemon dictionaries
    for k in ["my_active_pokemon", "opponent_active", "opponent_active_pokemon"]:
        if k in clone and isinstance(clone[k], dict):
            clone[k] = copy.deepcopy(clone[k])
                
    # Bench dictionaries (deep copy bench lists and nested dictionaries)
    for k in ["my_bench", "opponent_bench"]:
        if k in clone and isinstance(clone[k], list):
            clone[k] = [
                copy.deepcopy(p) if isinstance(p, dict) else p
                for p in clone[k]
            ]
    return clone

def apply_action(game_state: dict, action: str) -> dict:
    gs = fast_clone_state(game_state)
    hand = list(gs.get("my_hand", []))

    if action.endswith("_heads") or action.endswith("_tails"):
        _resolve_base(gs, hand, action)
        gs.pop("legal_actions", None)
        _regenerate_legal_actions(gs)
        _check_win_conditions(gs)
        return gs

    _resolve_base(gs, hand, action)
    gs.pop("legal_actions", None)
    _regenerate_legal_actions(gs)
    _check_win_conditions(gs)
    return gs
