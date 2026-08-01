"""
run_guided_helpers.py
Helper functions for managing training iteration states, refactoring, and PPO updates.
"""
import os
import json
import math
import logging
from pathlib import Path

try:
    import torch
    from torch.distributions import Categorical
except ImportError:
    torch = None
    Categorical = None

from scratch.run_guided_trajectory import _extract_all_steps
from scratch.run_guided_refactor import get_last_iteration_id, execute_refactor_step

logger = logging.getLogger("run_guided_helpers")
PPO_EPOCHS = 8
PPO_BATCH_SIZE = 256  # Reduced from 1024 to prevent Transformer OOM


from utils._compute_old_log_probs import _compute_old_log_probs


from utils.execute_ppo_step import execute_ppo_step


from utils.update_league_from_iteration import update_league_from_iteration
