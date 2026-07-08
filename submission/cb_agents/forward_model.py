import copy
import logging
from typing import Any

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

from cb_agents.forward_model_resolve import _resolve_base
from cb_agents.forward_model_gen import _regenerate_legal_actions, _check_win_conditions


def fast_clone_state(gs: dict) -> dict:
    clone = dict(gs)
    if "my_hand" in clone and isinstance(clone["my_hand"], list):
        clone["my_hand"] = list(clone["my_hand"])
    if "my_bench" in clone and isinstance(clone["my_bench"], list):
        clone["my_bench"] = [dict(p) if isinstance(p, dict) else p for p in clone["my_bench"]]
    if "legal_actions" in clone and isinstance(clone["legal_actions"], list):
        clone["legal_actions"] = list(clone["legal_actions"])
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
