import logging
from typing import Any

logger = logging.getLogger(__name__)

from cb_agents.forward_model_resolve import _resolve_base
from cb_agents.forward_model_gen import _regenerate_legal_actions, _check_win_conditions


def _fast_poke_clone(p: dict) -> dict:
    c = {}
    for k, v in p.items():
        if k == "attached" and isinstance(v, list):
            c[k] = list(v)
        elif isinstance(v, dict):
            c[k] = _fast_poke_clone(v)
        else:
            c[k] = v
    return c


def fast_clone_state(gs: dict) -> dict:
    clone = dict(gs)
    for k in ["my_hand", "my_discard", "opponent_discard", "my_deck", "opponent_deck", "my_prizes", "legal_actions"]:
        if k in clone and isinstance(clone[k], list):
            clone[k] = list(clone[k])

    if "my_decklist" in clone and isinstance(clone["my_decklist"], dict):
        clone["my_decklist"] = dict(clone["my_decklist"])

    for k in ["my_active_pokemon", "opponent_active", "opponent_active_pokemon"]:
        if k in clone and isinstance(clone[k], dict):
            clone[k] = _fast_poke_clone(clone[k])

    for k in ["my_bench", "opponent_bench"]:
        if k in clone and isinstance(clone[k], list):
            clone[k] = [_fast_poke_clone(p) if isinstance(p, dict) else p for p in clone[k]]
    return clone

def apply_action(game_state: dict, action: str) -> dict:
    gs = fast_clone_state(game_state)
    hand = list(gs.get("my_hand", []))

    _resolve_base(gs, hand, action)
    gs.pop("legal_actions", None)
    _regenerate_legal_actions(gs)
    _check_win_conditions(gs)
    return gs
