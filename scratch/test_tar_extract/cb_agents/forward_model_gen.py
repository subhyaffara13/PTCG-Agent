import random
from typing import Any

_ABILITY_DRAW = {"colress", "concealed", "flower selecting", "shining arcana"}

try:
    from cb_agents.card_registry import CardRegistry
except ImportError:
    CardRegistry = None


from utils._regenerate_legal_actions import _regenerate_legal_actions


from utils._check_win_conditions import _check_win_conditions


from utils._int_or_str import _int_or_str


from utils._remove_from_hand import _remove_from_hand


from utils._draw_cards import _draw_cards


from utils._apply_evolve import _apply_evolve
