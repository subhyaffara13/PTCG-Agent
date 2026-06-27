"""
factory/ppo_trainer_network.py

Defines the ActorCritic neural network architecture for PPO.
"""

import logging
from factory.state_dimensions import STATE_DIM

logger = logging.getLogger(__name__)

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch not available. ActorCritic model cannot be defined.")

if TORCH_AVAILABLE:
    class ActorCritic(nn.Module):
        """
        Shared feature extractor network with Actor and Critic heads.
        """
        def __init__(self, input_dim: int = STATE_DIM, hidden_dim: int = 256, action_dim: int = 3000):
            super().__init__()
            self.base = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.LayerNorm(hidden_dim),
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.ReLU(),
                nn.LayerNorm(hidden_dim // 2)
            )
            self.actor = nn.Sequential(
                nn.Linear(hidden_dim // 2, action_dim)
            )
            self.critic = nn.Sequential(
                nn.Linear(hidden_dim // 2, 1)
            )
            
        def forward(self, x):
            features = self.base(x)
            logits = self.actor(features)
            value = self.critic(features)
            return logits, value
else:
    class ActorCritic:
        def __init__(self, *args, **kwargs):
            pass
