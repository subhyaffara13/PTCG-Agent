import json
from pathlib import Path
from . import logger

def _save_checkpoint(iteration_id, model_path):
    if iteration_id is not None:
        try:
            from factory.model_checkpoint_manager import ModelCheckpointManager
            ModelCheckpointManager().save_checkpoint(model_path, iteration_id)
        except Exception as e:
            logger.warning(f"Failed to save model checkpoint: {e}")

def _save_metrics(iteration_id, rewards_t, actions_t, states_t):
    from factory.tensorboard_logger import TBLogger
    tb_logger = TBLogger.get()
    unique_actions = len(set(actions_t.tolist()))
    tb_logger.log_scalar("train/mean_reward", rewards_t.mean().item(), iteration_id)
    tb_logger.log_scalar("train/action_diversity", unique_actions, iteration_id)
    tb_logger.log_scalar("train/sample_count", len(states_t), iteration_id)
    tb_logger.flush()
    metrics_path = Path("models/ppo_metrics.json")
    metrics = {"iteration": iteration_id or 0, "mean_reward": rewards_t.mean().item(), "unique_actions": unique_actions}
    try:
        if metrics_path.exists():
            existing = json.loads(metrics_path.read_text(encoding="utf-8"))
            if isinstance(existing, list): existing.append(metrics)
            else: existing = [existing, metrics]
            metrics_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        else:
            metrics_path.write_text(json.dumps([metrics], indent=2), encoding="utf-8")
    except Exception as e:
        logger.debug(f"Could not save PPO metrics: {e}")
