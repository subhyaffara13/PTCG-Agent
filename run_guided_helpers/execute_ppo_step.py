from . import PPO_BATCH_SIZE, PPO_EPOCHS, Path, _extract_all_steps, json, logger, math, os, torch
from ._compute_old_log_probs import _compute_old_log_probs

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
                        steps_data = {}
                    
                    # Extract from the steps list in the Kaggle format dict
                    actual_steps = steps_data.get("steps", []) if isinstance(steps_data, dict) else steps_data
                    s, a = _extract_all_steps(actual_steps, aligner)
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
                            # step_data is [player0_dict, player1_dict]
                            step_data = actual_steps[t]
                            if isinstance(step_data, list) and len(step_data) >= 2:
                                p0 = step_data[0]
                                if isinstance(p0, dict):
                                    obs = p0.get("observation")
                                    if isinstance(obs, dict):
                                        current = obs.get("current")
                                        if isinstance(current, dict):
                                            players = current.get("players", [])
                                            if isinstance(players, list) and len(players) >= 2:
                                                my_idx = current.get("yourIndex", 0)
                                                if isinstance(my_idx, int) and my_idx < len(players):
                                                    p_mine_list = players[my_idx].get("prize", [])
                                                    p_opp_list = players[1 - my_idx].get("prize", [])
                                                    p_mine = len(p_mine_list) if isinstance(p_mine_list, list) else 0
                                                    p_opp = len(p_opp_list) if isinstance(p_opp_list, list) else 0
                                                    
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
                if total_steps + len(s) > 4000:
                    break
                states.extend(s)
                actions.extend(a)
                rewards.extend(r)
                total_steps += len(s)
                
            logger.info(f"Loaded {total_steps} sequential steps from {len(game_trajectories)} candidate trajectories.")
        except Exception as parse_err:
            logger.warning(f"Failed to parse iteration_result.json: {parse_err}")

        # Phase 3: Load historical trajectories from trajectory files
        try:
            from factory.trajectory_reader import TrajectoryReader
            reader = TrajectoryReader()
            recent_records = reader.load_recent(max_files=5)
            traj_data = reader.extract_training_data(recent_records)
            for s, a, r in traj_data:
                states.append(s)
                actions.append(a)
                rewards.append(r)
            logger.info(f"Loaded {len(traj_data)} additional training samples from trajectory files.")
        except Exception as e:
            logger.warning(f"Failed to load trajectories: {e}")
            
        if not states:
            logger.error("No real trajectory data loaded. Skipping PPO update.")
            return

        n = len(states)
        # Compute old_log_probs from the current policy instead of uniform constant
        if torch is not None and hasattr(ppo, 'model') and ppo.model is not None:
            model_old_log_probs = _compute_old_log_probs(ppo.model, ppo.device, states)
            if model_old_log_probs is not None:
                old_log_probs = model_old_log_probs
                logger.info(f"Computed old_log_probs from current policy (mean: {sum(old_log_probs)/len(old_log_probs):.4f})")
            else:
                old_log_probs = [math.log(1.0 / 3000)] * n
        else:
            old_log_probs = [math.log(1.0 / 3000)] * n
        logger.info(f"Loaded {n} state-action pairs. Running PPO...")
        
        # Determine winner from games
        winner_counts = {}
        for label, game in games.items():
            if isinstance(game, dict):
                w = game.get("winner")
                if w:
                    winner_counts[w] = winner_counts.get(w, 0) + 1
        improvement = winner_counts.get("player_a", 0) > winner_counts.get("player_b", 0)
        logger.info(f"Win summary: {winner_counts}  improvement={improvement}")
        
        ppo.update(states, actions, old_log_probs, rewards, epochs=PPO_EPOCHS, batch_size=PPO_BATCH_SIZE, iteration_id=iteration_id)
    except Exception as e:
        logger.error(f"Error during PPO update: {e}", exc_info=True)

