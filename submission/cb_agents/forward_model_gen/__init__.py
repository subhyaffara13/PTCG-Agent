import random
import json
from pathlib import Path
from typing import Any
import logging
from functools import lru_cache
logger = logging.getLogger(__name__)
from cb_agents.card_utils import _get_prize_yield, _int_or_str
from cb_agents.constants import ABILITY_DRAW as _ABILITY_DRAW
try:
    from cb_agents.card_registry import CardRegistry
except ImportError:
    CardRegistry = None
_LEGAL_CACHE_MAX = 512
from ._cache_legal_helpers import _legal_actions_cache, _legal_actions_cache_order

from ._cache_legal_helpers import _count_high_prize_on_board
from ._cache_legal_helpers import _cache_legal
from ._cache_legal_helpers import _legal_cache_key
from ._regenerate_legal_actions import _regenerate_legal_actions
from ._load_concede_thresholds__check_concede import _load_concede_thresholds
from ._load_concede_thresholds__check_concede import _check_concede
from ._check_win_conditions__remove_from_hand import _check_win_conditions
from ._check_win_conditions__remove_from_hand import _remove_from_hand
from ._draw_cards__apply_evolve import _draw_cards
from ._draw_cards__apply_evolve import _apply_evolve
