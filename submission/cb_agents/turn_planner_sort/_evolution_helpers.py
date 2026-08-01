import logging
from cb_agents.turn_planner_heuristics import _registry

logger = logging.getLogger(__name__)
_evo_cache = {}
_nn_instance = None

from utils._has_evolution_target import _has_evolution_target

from utils._get_neural_network import _get_neural_network

