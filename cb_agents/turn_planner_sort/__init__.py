import logging
import json
from typing import List
from pathlib import Path
from cb_agents.turn_planner_heuristics import _registry
from cb_agents.constants import SCALING_ATTACKERS
from cb_agents.heuristic_pipeline import _dead_weight_heuristic
logger = logging.getLogger(__name__)
_PRIORITY_RULES = []
try:
    for _pr_path in [Path("skills/priority_rules.json"), Path(__file__).resolve().parent.parent / "skills" / "priority_rules.json"]:
        if _pr_path.exists():
            _pr_data = json.loads(_pr_path.read_text(encoding="utf-8"))
            _PRIORITY_RULES = _pr_data.get("rules", [])
            break
except Exception:
    pass
_EARLY_BENCH_ORDER = ["play_trainer:", "ability:", "bench:", "retreat:", "attack:", "evolve:", "attach_energy:", "pass"]
from ._evolution_helpers import _nn_instance, _evo_cache

from ._evolution_helpers import _has_evolution_target
from ._evolution_helpers import _get_neural_network
from .sort_actions_heuristically import sort_actions_heuristically
