from typing import Any
from cb_agents.card_registry import CardRegistry
from utils._remove_from_hand import _remove_from_hand

def _apply_evolve(gs: dict, card_id: Any) -> None:
    from cb_agents.forward_model_gen_helpers import apply_evolve_helper
    apply_evolve_helper(gs, card_id, CardRegistry, _remove_from_hand)
