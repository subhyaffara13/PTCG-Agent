import logging
from typing import List
from cb_agents.turn_planner_heuristics import _registry, _SCALING_ATTACKERS
from cb_agents.heuristic_pipeline import _dead_weight_heuristic

logger = logging.getLogger(__name__)
_evo_cache = {}

from utils._has_evolution_target import _has_evolution_target

_EARLY_BENCH_ORDER = ["play_trainer:", "ability:", "bench:", "retreat:", "attack:", "evolve:", "attach_energy:", "pass"]

from utils.sort_actions_heuristically import sort_actions_heuristically
