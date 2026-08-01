"""
Sub-module: score_action, score_state
Delegates to C++ ptcg_core when available for maximum MCTS rollout speed.
"""
import logging
from cb_agents.card_registry import CardRegistry
from cb_agents.card_types import CardStage
logger = logging.getLogger(__name__)
_registry = CardRegistry()
_CARD_NAME_TO_ID = {}
_cards = getattr(_registry, "cards", None)
if _cards:
    for _sid, _sc in _cards.items():
        _CARD_NAME_TO_ID[_sc.card_name.lower()] = int(_sid) if not isinstance(_sid, int) else _sid
from cb_agents.card_utils import _get_prize_yield
try:
    import ptcg_core as _ptcg_core  # type: ignore
except Exception:
    _ptcg_core = None
_HAS_CPP_SCORE = False
_score_action_cache: dict = {}
_score_action_cache_keys: list = []
_SCORE_CACHE_MAX = 4096

from ._gs_cache_key_score_action__cache_score import _gs_cache_key
from ._gs_cache_key_score_action__cache_score import score_action
from ._gs_cache_key_score_action__cache_score import _cache_score
from ._score_action_python import _score_action_python
from .score_state import score_state
