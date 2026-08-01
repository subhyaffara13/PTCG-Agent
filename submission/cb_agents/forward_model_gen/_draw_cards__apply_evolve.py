from typing import Any
try:
    from cb_agents.card_registry import CardRegistry
except ImportError:
    CardRegistry = None
from ._check_win_conditions__remove_from_hand import _remove_from_hand

from utils._draw_cards import _draw_cards

from utils._apply_evolve import _apply_evolve

