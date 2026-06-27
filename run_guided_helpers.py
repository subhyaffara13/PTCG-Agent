"""
run_guided_helpers.py
Helper functions for managing training iteration states, refactoring, and PPO updates.
"""
import os
import json
import math
import logging
from pathlib import Path

from scratch.run_guided_trajectory import _extract_all_steps
from scratch.run_guided_refactor import get_last_iteration_id, execute_refactor_step

logger = logging.getLogger("run_guided_helpers")
PPO_EPOCHS = 4
PPO_BATCH_SIZE = 1024

def execute_ppo_step(iteration_id: int, iteration_result: dict = None):
    if os.environ.get("FAST_SIM_MODE") == "true":
        logger.info("FAST_SIM_MODE: Skipping PPO update to run at warp speed.")
        return
    logger.info(f"=== ITERATION {iteration_id}: EXECUTING PPO UPDATE ===")
    try:
        from factory.ppo_trainer import PPOTrainer
        from factory.data_alignment import DataAligner

        aligner = DataAligner()
        ppo = PPOTrainer()
        if not ppo.model:
            logger.warning("PPO Trainer model not initialized. Skipping.")
            return

        states, actions = [], []
        eval_path = Path("logs") / "iteration_result.json"
        if not eval_path.exists():
            logger.warning("No iteration_result.json found. Skipping PPO.")
            return
        try:
            raw_data = json.loads(eval_path.read_text(encoding="utf-8"))
            if raw_data is None:
                raw_data = {}
            games = raw_data.get("games", {})
            loaded_games = 0
            total_steps_loaded = 0
            for label, game in games.items():
                if not isinstance(game, dict):
                    continue
                log_files = game.get("log_files") or {}
                steps_file = log_files.get("steps")
                if not steps_file:
                    continue
                steps_path = Path("logs") / steps_file
                if not steps_path.exists():
                    continue
                try:
                    steps_data = json.loads(steps_path.read_text("utf-8"))
                    if steps_data is None:
                        steps_data = []
                    s, a = _extract_all_steps(steps_data, aligner)
                    if s:
                        states.extend(s); actions.extend(a)
                        loaded_games += 1
                        total_steps_loaded += len(s)
                except Exception as e:
                    logger.warning(f"Failed to load steps from {steps_path}: {e}")
            
            if len(states) > 5000:
                import random
                combined = list(zip(states, actions))
                random.shuffle(combined)
                combined = combined[:5000]
                states[:], actions[:] = zip(*combined)
                logger.info(f"Subsampled trajectories down to 5000 steps to speed up PPO update.")
                
            logger.info(f"Loaded {total_steps_loaded} steps from {loaded_games} games (out of {len(games)} total entries).")
        except Exception as parse_err:
            logger.warning(f"Failed to parse iteration_result.json: {parse_err}")

        if not states:
            logger.error("No real trajectory data loaded. Skipping PPO update to preserve learned weights.")
            return

        n = len(states)
        old_log_probs = [math.log(1.0 / 3000)] * n
        rewards = [0.0] * max(n - 1, 0) + [1.0]
        logger.info(f"Loaded {n} state-action pairs. Running PPO...")
        ppo.update(states, actions, old_log_probs, rewards, epochs=PPO_EPOCHS, batch_size=PPO_BATCH_SIZE)
    except Exception as e:
        logger.error(f"Error during PPO update: {e}", exc_info=True)
