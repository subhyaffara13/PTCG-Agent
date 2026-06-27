"""
factory/ppo_trainer.py

Proximal Policy Optimization (PPO) training loop. Kept under 100 lines.
"""

import os
import logging
from typing import List, Dict, Tuple

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
except ImportError:
    pass

from cb_agents.ppo_trainer_network import ActorCritic, TORCH_AVAILABLE
from cb_agents.ppo_trainer_update import run_ppo_update
from cb_agents.state_dimensions import STATE_DIM

logger = logging.getLogger(__name__)


class PPOTrainer:
    def __init__(self, state_dim: int = STATE_DIM, action_dim: int = 3000, model_path: str = 'models/ppo_actor_critic.pt'):
        self.state_dim, self.action_dim, self.model_path = state_dim, action_dim, model_path
        self.clip_ratio, self.gamma, self.lam, self.value_coef, self.entropy_coef = 0.2, 0.99, 0.95, 0.5, 0.02

        if TORCH_AVAILABLE:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = ActorCritic(state_dim, 256, action_dim).to(self.device)
            self.optimizer = optim.Adam(self.model.parameters(), lr=3e-4)
            if os.path.exists(model_path):
                try:
                    self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                    logger.info(f"Loaded existing PPO model from {model_path}")
                except Exception as e:
                    if "size mismatch" in str(e):
                        import time
                        import shutil
                        bak_path = f"{model_path}.bak_shape_mismatch_{int(time.time())}"
                        try:
                            shutil.move(model_path, bak_path)
                            logger.warning(f"Shape mismatch in {model_path}. Archived to {bak_path}. Initializing fresh model.")
                        except Exception as move_err:
                            logger.error(f"Failed to archive {model_path}: {move_err}")
                    else:
                        logger.warning(f"Could not load model: {e}")
                    self.model = ActorCritic(self.state_dim, 256, self.action_dim).to(self.device)
                    self.optimizer = optim.Adam(self.model.parameters(), lr=3e-4)
            logger.info(f"Initialized PPOTrainer on {self.device}")
        else:
            self.model = None

    def update(self, states: List[List[float]], actions: List[int], old_log_probs: List[float],
               rewards: List[float], epochs: int = 4, batch_size: int = 1024):
        if not TORCH_AVAILABLE or not states:
            logger.error("Cannot train: PyTorch missing or empty states.")
            return
        run_ppo_update(self.model, self.optimizer, states, actions, old_log_probs, rewards,
                       self.clip_ratio, self.gamma, self.lam, self.value_coef, self.entropy_coef,
                       self.device, epochs, batch_size, self.model_path)
