from typing import Any
try:
    from cb_agents.card_registry import CardRegistry
except ImportError:
    CardRegistry = None
from ._check_win_conditions__remove_from_hand import _remove_from_hand

def _draw_cards(hand: list, gs: dict, n: int) -> list:
    dc = gs.get("my_deck_count", 60)
    drawn = min(n, dc)
    gs["my_deck_count"] = dc - drawn
    if n > dc:
        gs["deck_out_loss"] = True
    return hand + [0] * drawn

def _apply_evolve(gs: dict, card_id: Any) -> None:
    from cb_agents.forward_model_gen_helpers import apply_evolve_helper
    apply_evolve_helper(gs, card_id, CardRegistry, _remove_from_hand)

