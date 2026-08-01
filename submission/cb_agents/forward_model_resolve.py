from typing import Any

from cb_agents.forward_model_gen import _remove_from_hand, _apply_evolve, _draw_cards
from cb_agents.card_utils import _int_or_str
from cb_agents.constants import ABILITY_DRAW
from cb_agents.card_registry import CardRegistry


from utils._resolve_base import _resolve_base
