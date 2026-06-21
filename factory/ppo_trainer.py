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
    from torch.distributions import Categorical
except ImportError:
    pass

from factory.ppo_trainer_network import ActorCritic, TORCH_AVAILABLE

logger = logging.getLogger(__name__)


class PPOTrainer:
    def __init__(self, state_dim: int = 71, action_dim: int = 3000, model_path: str = 'models/ppo_actor_critic.pt'):
        self.state_dim, self.action_dim, self.model_path = state_dim, action_dim, model_path
        self.clip_ratio, self.gamma, self.lam, self.value_coef, self.entropy_coef = 0.2, 0.99, 0.95, 0.5, 0.01
        
        if TORCH_AVAILABLE:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = ActorCritic(state_dim, 256, action_dim).to(self.device)
            self.optimizer = optim.Adam(self.model.parameters(), lr=3e-4)
            if os.path.exists(model_path):
                try:
                    self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                    logger.info(f"Loaded existing PPO model from {model_path}")
                except Exception as e:
                    logger.warning(f"Could not load existing model: {e}")
            logger.info(f"Initialized PPOTrainer on {self.device}")
        else:
            self.model = None

    def _compute_gae(self, rewards: "torch.Tensor", values: "torch.Tensor") -> Tuple["torch.Tensor", "torch.Tensor"]:
        advantages = torch.zeros_like(rewards)
        last_adv = 0
        padded_values = torch.cat([values, torch.tensor([0.0]).to(self.device)])
        for t in reversed(range(len(rewards))):
            delta = rewards[t] + self.gamma * padded_values[t + 1] - padded_values[t]
            advantages[t] = last_adv = delta + self.gamma * self.lam * last_adv
        return advantages, advantages + values

    def update(self, states: List[List[float]], actions: List[int], old_log_probs: List[float],
               rewards: List[float], epochs: int = 4, batch_size: int = 64):
        if not TORCH_AVAILABLE or not states:
            logger.error("Cannot train: PyTorch missing or empty states.")
            return
            
        states_t = torch.FloatTensor(states).to(self.device)
        actions_t = torch.LongTensor(actions).to(self.device)
        old_log_probs_t = torch.FloatTensor(old_log_probs).to(self.device)
        rewards_t = torch.FloatTensor(rewards).to(self.device)
        
        self.model.eval()
        with torch.no_grad():
            _, values_t = self.model(states_t)
            values_t = values_t.squeeze(-1)
            
        advantages_t, returns_t = self._compute_gae(rewards_t, values_t)
        advantages_t = (advantages_t - advantages_t.mean()) / (advantages_t.std() + 1e-8)
        
        self.model.train()
        size = len(states_t)
        indices = torch.arange(size)
        
        for epoch in range(epochs):
            indices = indices[torch.randperm(size)]
            for start in range(0, size, batch_size):
                idx = indices[start:start + batch_size]
                logits, b_values = self.model(states_t[idx])
                b_values = b_values.squeeze(-1)
                
                dist = Categorical(logits=logits)
                new_log_probs = dist.log_prob(actions_t[idx])
                ratio = torch.exp(new_log_probs - old_log_probs_t[idx])
                surr1 = ratio * advantages_t[idx]
                surr2 = torch.clamp(ratio, 1.0 - self.clip_ratio, 1.0 + self.clip_ratio) * advantages_t[idx]
                
                loss = -torch.min(surr1, surr2).mean() + self.value_coef * nn.MSELoss()(b_values, returns_t[idx]) - self.entropy_coef * dist.entropy().mean()
                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=0.5)
                self.optimizer.step()
                
        os.makedirs('models', exist_ok=True)
        torch.save(self.model.state_dict(), self.model_path)
        logger.info(f"PPO update complete. Model saved to {self.model_path}")
