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
PPO_EPOCHS = 8
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

        states, actions, rewards = [], [], []
        eval_path = Path("logs") / "iteration_result.json"
        if not eval_path.exists():
            logger.warning("No iteration_result.json found. Skipping PPO.")
            return
        try:
            raw_data = json.loads(eval_path.read_text(encoding="utf-8"))
            if raw_data is None:
                raw_data = {}
            games = raw_data.get("games", {})
            
            # List of (game_states, game_actions, game_rewards) tuples
            game_trajectories = []
            
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
                    if not s:
                        continue
                    
                    winner = game.get("winner")  # "player_a", "player_b", "draw"
                    game_len = len(s)
                    
                    # Dense Reward Assignment:
                    # Final outcome reward (+10.0 / -10.0)
                    game_rew = [0.0] * game_len
                    if winner == "player_a":
                        game_rew[-1] = 10.0
                    elif winner == "player_b":
                        game_rew[-1] = -10.0
                        
                    # Intermediate Prize Rewards
                    prev_p_mine, prev_p_opp = 6, 6
                    for t in range(game_len):
                        try:
                            step_data = steps_data[t]
                            players = step_data.get("players", [])
                            if len(players) >= 2:
                                p0_prize = len(players[0].get("observation", {}).get("prize", []))
                                p1_prize = len(players[1].get("observation", {}).get("prize", []))
                                p_mine = p0_prize
                                p_opp = p1_prize
                                
                                # We took a prize card: +2.0
                                if p_opp < prev_p_opp:
                                    game_rew[t] += 2.0 * (prev_p_opp - p_opp)
                                # Opponent took a prize card: -2.0
                                if p_mine < prev_p_mine:
                                    game_rew[t] -= 2.0 * (prev_p_mine - p_mine)
                                    
                                prev_p_mine, prev_p_opp = p_mine, p_opp
                        except Exception:
                            pass
                            
                    game_trajectories.append((s, a, game_rew))
                except Exception as e:
                    logger.warning(f"Failed to load steps from {steps_path}: {e}")
            
            # Subsample by keeping whole game trajectories intact (retaining sequence coherence)
            import random
            random.shuffle(game_trajectories)
            
            total_steps = 0
            for s, a, r in game_trajectories:
                if total_steps + len(s) > 8000:
                    break
                states.extend(s)
                actions.extend(a)
                rewards.extend(r)
                total_steps += len(s)
                
            logger.info(f"Loaded {total_steps} sequential steps from {len(game_trajectories)} candidate trajectories.")
        except Exception as parse_err:
            logger.warning(f"Failed to parse iteration_result.json: {parse_err}")
            
        if not states:
            logger.error("No real trajectory data loaded. Skipping PPO update.")
            return

        n = len(states)
        old_log_probs = [math.log(1.0 / 3000)] * n
        logger.info(f"Loaded {n} state-action pairs. Running PPO...")
        ppo.update(states, actions, old_log_probs, rewards, epochs=PPO_EPOCHS, batch_size=PPO_BATCH_SIZE)
    except Exception as e:
        logger.error(f"Error during PPO update: {e}", exc_info=True)
