
def run_master_loop(enable_distributed=True):
    logger.info("Orchestration Agent (Master Mode) started." if enable_distributed else "Orchestration Agent (Local Mode) started.")
    
    # Initialize and start centralized InferenceServer
    inference_server = None
    try:
        from cb_agents.value_network_helpers import state_to_tensor, state_to_card_tokens, HAS_TORCH
        if HAS_TORCH:
            from factory.ppo_trainer_network import ActorCritic
            from factory.state_dimensions import STATE_DIM
            import torch
            import os
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model_path = "models/ppo_actor_critic.pt"
            model = None
            if os.path.exists(model_path):
                model = ActorCritic(input_dim=STATE_DIM, hidden_dim=256, action_dim=3000)
                model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
                model.to(device)
                logger.info("Loaded PPO model for InferenceServer.")
                
            from factory.inference_server import InferenceServer
            inference_server = InferenceServer(model, device=device, state_to_tensor=state_to_tensor, state_to_card_tokens=state_to_card_tokens)
            inference_server.start()
    except Exception as e:
        logger.warning(f"Failed to start InferenceServer: {e}")
        
    beacon = None
    if enable_distributed:
        version = get_local_version() or "unknown"
        beacon = MasterBeacon(code_version=version)
        beacon.start()
        from distributed.log_sync import LogCollectorServer
        LogCollectorServer().start()
    
    scripts = get_training_scripts(enable_distributed=enable_distributed)
    iteration = 0
    # Outer try-except-finally block to ensure graceful shutdown of MasterBeacon
    try:
        while True:
            logger.info("--- [Train Phase] Starting distributed master and PPO workers ---" if enable_distributed else "--- [Train Phase] Starting local training processes ---")
            processes = launch_processes(scripts)
            try:
                # Monitor processes for up to 10 minutes (10 * 60 seconds)
                for _ in range(10):
                    monitor_and_restart(processes, scripts)
                    time.sleep(60)
            except KeyboardInterrupt:
                logger.info("Train phase monitoring loop interrupted. Proceeding to training process cleanup and main loop exit.")
                # We re-raise to ensure the script actually terminates, instead of just breaking the inner loop.
                raise
            finally:
                logger.info("--- [Halt Phase] Stopping training processes ---")
                try:
                    cleanup(processes)
                    time.sleep(2)
                except KeyboardInterrupt:
                    logger.info("Ignored extra Ctrl+C during training process cleanup. Continuing safe shutdown.")

            # These phases run every 10 minutes to trigger continuous LLM meta-learning, replay analysis, and evolution
            logger.info("--- [Analytics Phase] Running synchronous checks ---")
            from factory.log_pruner import prune_logs
            prune_logs(max_files=1000)
            
            # --- TRUE AUTOMATION: RL & EVOLUTION ---

            try:
                from factory.teams.development_team import DevelopmentTeam
                DevelopmentTeam().run_development(iteration)
            except Exception as e:
                logger.error(f"Development Team cycle failed: {e}", exc_info=True)

            run_hourly_checks(iteration)
            run_analytics_check(iteration)
            
            # Log league Elo ratings to TensorBoard
            try:
                from factory.league_manager import LeagueManager
                from factory.tensorboard_logger import TBLogger
                lm = LeagueManager()
                tb = TBLogger.get()
                for agent_name, rating in lm.ratings.items():
                    tb.log_scalar(f"league_elo/{agent_name}", rating, iteration)
                tb.flush()
                logger.info("Logged league ELO ratings to TensorBoard.")
            except Exception as e:
                logger.debug(f"Failed to log ELO: {e}")
            
            if enable_distributed:
                try:
                    from factory.orchestrator_master_git import auto_commit_and_push_if_changed
                    auto_commit_and_push_if_changed()
                except Exception as e:
                    logger.error(f"Git auto-push failed: {e}")
                
            iteration += 1
    except KeyboardInterrupt:
        logger.info("Orchestration Agent (Master Mode) received KeyboardInterrupt. Initiating graceful shutdown.")
        raise
    except Exception as e:
        # Catch any other unexpected exceptions and log them with stack trace
        logger.error(f"Orchestration Agent (Master Mode) crashed due to unhandled exception: {e}", exc_info=True)
    finally:
        if beacon:
            logger.info("Stopping MasterBeacon...")
            beacon.stop()
        if inference_server:
            logger.info("Stopping InferenceServer...")
            inference_server.stop()
        logger.info("Orchestration Agent (Master Mode) shutdown complete.")

