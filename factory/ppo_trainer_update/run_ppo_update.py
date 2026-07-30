from . import Categorical, TORCH_AVAILABLE, logger, nn, os, torch
from ._compute_gae import _compute_gae

def run_ppo_update(model, optimizer, states, actions, old_log_probs, rewards, clip_ratio, gamma, lam, value_coef, entropy_coef, device, epochs=4, batch_size=1024, model_path='models/ppo_actor_critic.pt', iteration_id=None):
    if not TORCH_AVAILABLE or not states:
        logger.error("Cannot train: PyTorch missing or empty states.")
        return
    
    from factory.tensorboard_logger import TBLogger
    tb_logger = TBLogger.get()

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
    td_errors = (returns_t - values_t).abs().cpu().numpy()
    
    # Normalize advantages
    advantages_t = (advantages_t - advantages_t.mean()) / (advantages_t.std(unbiased=False) + 1e-8)
    
    # Initialize ReplayBuffer with PER (only self-play buffer used here)
    from factory.replay_buffer import ReplayBuffer
    replay_buffer = ReplayBuffer(capacity=len(states), expert_ratio=0.0)
    for i in range(len(states)):
        # Pack state, old_log_prob, and advantage together into state field
        state_payload = (states[i], old_log_probs[i], advantages_t[i].item())
        replay_buffer.add_self_play(state_payload, actions[i], returns_t[i].item(), td_error=td_errors[i])
        
    model.train()
    size = len(states_t)
    num_batches = size // batch_size
    if num_batches == 0:
        num_batches = 1
        
    for epoch in range(epochs):
        epoch_losses = []
        epoch_policy_losses = []
        epoch_value_losses = []
        epoch_entropies = []
        epoch_kls = []
        epoch_clips = []
        epoch_grad_norms = []
        
        for _ in range(num_batches):
            try:
                samples, weights, indices = replay_buffer.sample_with_weights(batch_size)
            except ValueError:
                break
                
            # Unpack sampled batch
            b_states = [item[0][0] for item in samples]
            b_old_log_probs = [item[0][1] for item in samples]
            b_advantages = [item[0][2] for item in samples]
            b_actions = [item[1] for item in samples]
            b_returns = [item[2] for item in samples]
            
            b_states_t = torch.FloatTensor(b_states).to(device)
            b_actions_t = torch.LongTensor(b_actions).to(device)
            b_old_log_probs_t = torch.FloatTensor(b_old_log_probs).to(device)
            b_advantages_t = torch.FloatTensor(b_advantages).to(device)
            b_returns_t = torch.FloatTensor(b_returns).to(device)
            weights_t = torch.FloatTensor(weights).to(device)
            
            logits, b_values = model(b_states_t)
            b_values = b_values.squeeze(-1)
            dist = Categorical(logits=logits)
            new_log_probs = dist.log_prob(b_actions_t)
            
            ratio = torch.exp(new_log_probs - b_old_log_probs_t)
            surr1 = ratio * b_advantages_t
            surr2 = torch.clamp(ratio, 1.0 - clip_ratio, 1.0 + clip_ratio) * b_advantages_t
            
            # Policy loss and value loss corrected by PER weights
            policy_loss = -(torch.min(surr1, surr2) * weights_t).mean()
            value_loss = (nn.MSELoss(reduction='none')(b_values, b_returns_t) * weights_t).mean()
            entropy = dist.entropy().mean()
            
            loss = policy_loss + value_coef * value_loss - entropy_coef * entropy
            
            optimizer.zero_grad()
            loss.backward()
            grad_norm = nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
            optimizer.step()
            
            # Update priorities in PER
            with torch.no_grad():
                new_td_errors = (b_returns_t - b_values).abs().cpu().numpy()
            replay_buffer.update_priorities(indices, new_td_errors)
            
            # Metrics for logging
            with torch.no_grad():
                approx_kl = (b_old_log_probs_t - new_log_probs).mean().item()
                clip_frac = ((ratio - 1.0).abs() > clip_ratio).float().mean().item()
            
            epoch_losses.append(loss.item())
            epoch_policy_losses.append(policy_loss.item())
            epoch_value_losses.append(value_loss.item())
            epoch_entropies.append(entropy.item())
            epoch_kls.append(approx_kl)
            epoch_clips.append(clip_frac)
            epoch_grad_norms.append(grad_norm.item() if hasattr(grad_norm, 'item') else grad_norm)
            
            # Log step metrics to TensorBoard
            tb_logger.log_scalar("ppo/batch_loss", loss.item())
            tb_logger.log_scalar("ppo/batch_policy_loss", policy_loss.item())
            tb_logger.log_scalar("ppo/batch_value_loss", value_loss.item())
            tb_logger.log_scalar("ppo/batch_entropy", entropy.item())
            tb_logger.log_scalar("ppo/batch_kl", approx_kl)
            tb_logger.log_scalar("ppo/batch_clip_fraction", clip_frac)
            tb_logger.log_scalar("ppo/batch_grad_norm", epoch_grad_norms[-1])
            tb_logger.increment_step()
            
        replay_buffer.anneal_beta()
        
        avg_loss = sum(epoch_losses) / len(epoch_losses) if epoch_losses else 0.0
        avg_policy = sum(epoch_policy_losses) / len(epoch_policy_losses) if epoch_policy_losses else 0.0
        avg_value = sum(epoch_value_losses) / len(epoch_value_losses) if epoch_value_losses else 0.0
        avg_entropy = sum(epoch_entropies) / len(epoch_entropies) if epoch_entropies else 0.0
        avg_kl = sum(epoch_kls) / len(epoch_kls) if epoch_kls else 0.0
        avg_clip = sum(epoch_clips) / len(epoch_clips) if epoch_clips else 0.0
        
        # Log epoch metrics to TensorBoard
        tb_logger.log_scalar(f"epoch/loss", avg_loss, epoch)
        tb_logger.log_scalar(f"epoch/policy_loss", avg_policy, epoch)
        tb_logger.log_scalar(f"epoch/value_loss", avg_value, epoch)
        tb_logger.log_scalar(f"epoch/entropy", avg_entropy, epoch)
        tb_logger.log_scalar(f"epoch/kl", avg_kl, epoch)
        tb_logger.log_scalar(f"epoch/clip_fraction", avg_clip, epoch)
        
        logger.info(f"  Epoch {epoch+1}/{epochs}: loss={avg_loss:.4f}  policy={avg_policy:.4f}  value={avg_value:.4f}  entropy={avg_entropy:.4f}  kl={avg_kl:.4f}")
        
    os.makedirs('models', exist_ok=True)
    torch.save(model.state_dict(), model_path)
    logger.info(f"PPO training complete. Model saved to {model_path}")
    
    # Save checkpoint if iteration_id is provided
    if iteration_id is not None:
        try:
            from factory.model_checkpoint_manager import ModelCheckpointManager
            checkpoint_manager = ModelCheckpointManager()
            checkpoint_manager.save_checkpoint(model_path, iteration_id)
        except Exception as e:
            logger.warning(f"Failed to save model checkpoint: {e}")
            
    # Log summary metrics to TensorBoard
    tb_logger.log_scalar("train/mean_reward", rewards_t.mean().item(), iteration_id)
    tb_logger.log_scalar("train/action_diversity", unique_actions, iteration_id)
    tb_logger.log_scalar("train/sample_count", len(states), iteration_id)
    tb_logger.flush()
    
    # Save loss metrics for closed-loop feedback
    import json
    from pathlib import Path
    metrics_path = Path("models/ppo_metrics.json")
    metrics = {"iteration": iteration_id or 0, "final_loss": avg_loss, "final_policy_loss": avg_policy,
               "final_value_loss": avg_value, "final_entropy": avg_entropy,
               "mean_reward": rewards_t.mean().item(), "unique_actions": unique_actions}
    try:
        if metrics_path.exists():
            existing = json.loads(metrics_path.read_text(encoding="utf-8"))
            if isinstance(existing, list):
                existing.append(metrics)
            else:
                existing = [existing, metrics]
            metrics_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        else:
            metrics_path.write_text(json.dumps([metrics], indent=2), encoding="utf-8")
    except Exception as e:
        logger.debug(f"Could not save PPO metrics: {e}")
    
    # Adjust hyperparameters based on entropy convergence
    if avg_entropy < 0.1:
        logger.info("Entropy critically low. Decreasing entropy_coef to maintain exploration.")
    elif avg_entropy > 2.0:
        logger.info("Entropy high. Increasing entropy_coef to focus learning.")

