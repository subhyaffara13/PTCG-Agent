import os
import logging
from typing import List

logger = logging.getLogger(__name__)

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.distributions import Categorical
except ImportError:
    pass

from factory.ppo_trainer_network import TORCH_AVAILABLE


def _compute_gae(rewards, values, device, gamma=0.99, lam=0.95):
    advantages = torch.zeros_like(rewards)
    last_adv = 0
    padded_values = torch.cat([values, torch.tensor([0.0]).to(device)])
    for t in reversed(range(len(rewards))):
        delta = rewards[t] + gamma * padded_values[t + 1] - padded_values[t]
        advantages[t] = last_adv = delta + gamma * lam * last_adv
    return advantages, advantages + values


def run_ppo_update(model, optimizer, states, actions, old_log_probs, rewards, clip_ratio, gamma, lam, value_coef, entropy_coef, device, epochs=4, batch_size=1024, model_path='models/ppo_actor_critic.pt'):
    if not TORCH_AVAILABLE or not states:
        logger.error("Cannot train: PyTorch missing or empty states.")
        return
    states_t = torch.FloatTensor(states).to(device)
    actions_t = torch.LongTensor(actions).to(device)
    old_log_probs_t = torch.FloatTensor(old_log_probs).to(device)
    rewards_t = torch.FloatTensor(rewards).to(device)
    logger.info(f"  Training on {len(states)} samples, {epochs} epochs, batch_size={batch_size}")
    logger.info(f"  Mean reward: {rewards_t.mean().item():.4f}, range: [{rewards_t.min().item():.4f}, {rewards_t.max().item():.4f}]")
    unique_actions = len(set(actions))
    logger.info(f"  Action diversity: {unique_actions} unique actions across {len(actions)} samples; entropy_coef={entropy_coef}")
    model.eval()
    with torch.no_grad():
        _, values_t = model(states_t)
        values_t = values_t.squeeze(-1)
    advantages_t, returns_t = _compute_gae(rewards_t, values_t, device, gamma, lam)
    advantages_t = (advantages_t - advantages_t.mean()) / (advantages_t.std(unbiased=False) + 1e-8)
    model.train()
    size = len(states_t)
    indices = torch.arange(size)
    for epoch in range(epochs):
        indices = indices[torch.randperm(size)]
        epoch_losses = []
        epoch_policy_losses = []
        epoch_value_losses = []
        epoch_entropies = []
        for start in range(0, size, batch_size):
            idx = indices[start:start + batch_size]
            logits, b_values = model(states_t[idx])
            b_values = b_values.squeeze(-1)
            dist = Categorical(logits=logits)
            new_log_probs = dist.log_prob(actions_t[idx])
            ratio = torch.exp(new_log_probs - old_log_probs_t[idx])
            surr1 = ratio * advantages_t[idx]
            surr2 = torch.clamp(ratio, 1.0 - clip_ratio, 1.0 + clip_ratio) * advantages_t[idx]
            policy_loss = -torch.min(surr1, surr2).mean()
            value_loss = nn.MSELoss()(b_values, returns_t[idx])
            entropy = dist.entropy().mean()
            loss = policy_loss + value_coef * value_loss - entropy_coef * entropy
            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
            optimizer.step()
            epoch_losses.append(loss.item())
            epoch_policy_losses.append(policy_loss.item())
            epoch_value_losses.append(value_loss.item())
            epoch_entropies.append(entropy.item())
        avg_loss = sum(epoch_losses) / len(epoch_losses)
        avg_policy = sum(epoch_policy_losses) / len(epoch_policy_losses)
        avg_value = sum(epoch_value_losses) / len(epoch_value_losses)
        avg_entropy = sum(epoch_entropies) / len(epoch_entropies)
        logger.info(f"  Epoch {epoch+1}/{epochs}: loss={avg_loss:.4f}  policy={avg_policy:.4f}  value={avg_value:.4f}  entropy={avg_entropy:.4f}")
    os.makedirs('models', exist_ok=True)
    torch.save(model.state_dict(), model_path)
    logger.info(f"PPO training complete. Model saved to {model_path}")
