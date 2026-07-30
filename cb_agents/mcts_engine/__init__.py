import logging
from typing import List
import os
from cb_agents.value_network import (
    BaseValueNetwork, BasePolicyNetwork,
    HeuristicValueNetwork, HeuristicPolicyNetwork,
    ActionPrior,
)
from cb_agents.heuristic_pipeline import pipeline
from cb_agents.mcts_node import MCTSNode
from cb_agents.mcts_parallel import MCTSParallelMixin
from cb_agents.mcts_selection import MCTSSelectionMixin
from cb_agents.mcts_mast import MASTPolicy
from cb_agents.state_cache import TranspositionTable
logger = logging.getLogger(__name__)
try:
    import ptcg_core  # type: ignore
    HAS_CPP = True
except Exception:
    ptcg_core = None
    HAS_CPP = False
is_kaggle = any(k.startswith("KAGGLE") for k in os.environ) or not os.path.exists("build_submission.py")
if not HAS_CPP:
    if is_kaggle:
        logger.info("Running on Kaggle: C++ extension not found. Using pure Python MCTS fallback.")
    else:
        logger.info("ptcg_core C++ extension not found. Using pure Python MCTS.")
else:
    logger.info("ptcg_core C++ extension successfully loaded. Running with fast C++ MCTS!")

from ._to_cpp_compatible_state import _to_cpp_compatible_state
from .mctsengine import MCTSEngine
