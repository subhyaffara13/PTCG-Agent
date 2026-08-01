import logging
from typing import List
from cb_agents.card_registry import CardRegistry
from cb_agents.card_types import CardStage

logger = logging.getLogger(__name__)
_registry = CardRegistry()

_ABILITY_DRAW_KEYWORDS = {"colress", "concealed cards", "shining arcana", "flower selecting"}

_SEARCH_KEYWORDS = {"nest ball", "ultra ball", "quick ball", "level ball",
                    "secret box", "mega signal", "team rocket's petrel", "surfing beach"}

_SCALING_ATTACKERS = {"raging bolt", "iron hands", "chien pao", "ceruledge",
                      "garchomp", "roaring moon", "groudon", "kyogre"}

from utils._hand_strength import _hand_strength

from utils._has_dead_weight import _has_dead_weight

from utils.has_draw_remaining import has_draw_remaining

from cb_agents.heuristic_pipeline import _thinning_value, _pick_best_search, _dead_weight_heuristic, check_mcts_bypass
from cb_agents.turn_planner_sort import _has_evolution_target, sort_actions_heuristically, _EARLY_BENCH_ORDER
