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
def get_last_iteration_id() -> int:
    try:
        report_path = Path("logs/eval_report.json")
        if report_path.exists():
            data = json.loads(report_path.read_text(encoding="utf-8"))
            return data.get("iteration", 0)
    except Exception:
        pass
    return 0

def execute_refactor_step(iteration_id: int):
    pass

def _extract_all_steps(*args, **kwargs):
    pass
logger = logging.getLogger("run_guided_helpers")
PPO_EPOCHS = 8
PPO_BATCH_SIZE = 256  # Reduced from 1024 to prevent Transformer OOM

from ._compute_old_log_probs import _compute_old_log_probs
from .execute_ppo_step import execute_ppo_step
from .update_league_from_iteration import update_league_from_iteration
