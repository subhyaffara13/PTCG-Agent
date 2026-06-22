"""
run_guided_helpers.py

Helper functions for managing training iteration states, refactoring, and PPO updates.
"""

import sys
import json
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger("run_guided_helpers")

def get_last_iteration_id() -> int:
    eval_report = Path("logs/eval_report.json")
    if eval_report.exists():
        try:
            data = json.loads(eval_report.read_text(encoding="utf-8"))
            return int(data.get("iteration", 90))
        except Exception as e:
            logger.warning(f"Failed to read iteration ID from eval_report: {e}")
    return 90

def execute_refactor_step(iteration_id: int):
    logger.info(f"=== ITERATION {iteration_id}: INITIATING REFACTOR/CLEANUP STEP ===")
    logger.info("Running pytest suite...")
    try:
        res = subprocess.run(["pytest"], capture_output=True, text=True, check=True)
        logger.info(f"Pytest passed:\n{res.stdout[-500:]}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Pytest failed during refactor step!\n{e.stderr}\n{e.stdout}")
        
    logger.info("Re-building submission package...")
    try:
        res = subprocess.run([sys.executable, "build_submission.py"], capture_output=True, text=True, check=True)
        logger.info(res.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"build_submission.py failed: {e.stderr}")

def execute_ppo_step(iteration_id: int):
    import os
    if os.environ.get("FAST_SIM_MODE") == "true":
        logger.info("FAST_SIM_MODE: Skipping PPO update to run at warp speed.")
        return
    logger.info(f"=== ITERATION {iteration_id}: EXECUTING PPO UPDATE ===")
    try:
        from factory.ppo_trainer import PPOTrainer
        from factory.data_alignment import DataAligner
        import math
        
        eval_path = Path("logs") / "iteration_result.json"
        if not eval_path.exists():
            logger.warning("No iteration_result.json found. Skipping PPO.")
            return
            
        aligner = DataAligner()
        ppo = PPOTrainer()
        if not ppo.model:
            logger.warning("PPO Trainer model not initialized. Skipping.")
            return
            
        states, actions = [], []
        try:
            raw_data = json.loads(eval_path.read_text(encoding="utf-8"))
            for step in raw_data.get("steps_dump", []):
                states.append(aligner.normalize_state(step.get("state", {})))
                actions.append(aligner.normalize_action(step.get("action", "")))
        except Exception as parse_err:
            logger.warning(f"Failed to parse iteration_result.json steps: {parse_err}")

        if not states:
            logger.warning("No real trajectory data found. Using mock fallback.")
            states = [[0.5] * 71 for _ in range(30)]
            actions = [1] * 30
        
        n = len(states)
        old_log_probs = [math.log(1.0 / 3000)] * n
        rewards = [0.0] * max(n - 1, 0) + [1.0]

        logger.info(f"Loaded {n} state-action pairs. Running PPO...")
        ppo.update(states, actions, old_log_probs, rewards, epochs=2)
    except Exception as e:
        logger.error(f"Error during PPO update: {e}", exc_info=True)
