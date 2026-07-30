"""
factory/hyperparam_scheduler.py

Dynamic hyperparameter annealing for PPO training and Optuna-based
hyperparameter tuning for MCTS parameters (c_puct, exploration rates, utility weights).
"""
import json
import math
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Callable
logger = logging.getLogger(__name__)
try:
    import optuna
    OPTUNA_AVAILABLE = True
except ImportError:
    optuna = None
    OPTUNA_AVAILABLE = False

from .optunamctstuner import OptunaMCTSTuner
from .hyperparamscheduler import HyperparamScheduler
