import copy
import logging
from typing import Any

logger = logging.getLogger(__name__)

_ABILITY_DRAW = {"colress", "concealed", "flower selecting", "shining arcana"}

from agents.forward_model_resolve import _resolve_base
from agents.forward_model_gen import _regenerate_legal_actions, _check_win_conditions


def apply_action(game_state: dict, action: str) -> dict:
    gs = copy.deepcopy(game_state)
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
