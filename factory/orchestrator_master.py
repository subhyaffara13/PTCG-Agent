import time
import logging
from factory.orchestration_agent_helpers import auto_submit_if_ready, run_analytics_check
from factory.orchestration_agent_utils import get_training_scripts
from factory.orchestration_process import launch_processes, monitor_and_restart, cleanup, script_log_path
from distributed.discovery import MasterBeacon
from distributed.code_sync import get_local_version
import sys
import subprocess

logger = logging.getLogger("orchestration_agent")

def run_hourly_checks(iteration: int):
    """Runs leaderboard checks and auto-submission logic."""
    logger.info(f"--- [Orchestration] Hourly check #{iteration} ---")
    
    import os
    if not os.path.exists(".env") and not os.path.exists("kaggle.json"):
        logger.error("WARNING: Missing .env or kaggle.json! This worker promoted to Master but lacks Kaggle credentials. Skipping submissions.")
        return

    for script in ["scratch/check_submissions.py", "scratch/run_leaderboard_loop.py"]:
        log_path = script_log_path(script)
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                subprocess.run([sys.executable, script], stdout=f, stderr=f, check=True)
        except Exception as e:
            logger.error(f"Error running {script}: {e}")

    try:
        auto_submit_if_ready()
    except Exception as e:
        logger.error(f"Auto-submission error: {e}")

    # Run Kaggle Replay self-healing check using AnalyticsTeam
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        subs = api.competition_submissions("pokemon-tcg-ai-battle")
        if subs:
            subs.sort(key=lambda s: s.date, reverse=True)
            latest_sub = subs[0]
            sub_id = getattr(latest_sub, 'ref', None)
            if not sub_id:
                for attr in ['id', 'submission_id', 'submissionId', 'key']:
                    if hasattr(latest_sub, attr):
                        sub_id = getattr(latest_sub, attr)
                        break
            if sub_id:
                logger.info(f"Triggering AnalyticsTeam replay audit for Kaggle submission {sub_id}...")
                from factory.teams.analytics_team import AnalyticsTeam
                AnalyticsTeam().run_kaggle_analysis(sub_id)
            else:
                logger.warning("Could not find submission ID for latest submission.")
    except Exception as e:
        logger.error(f"Error running AnalyticsTeam Kaggle self-healing audit: {e}")

def run_master_loop(enable_distributed=True):
    logger.info("Orchestration Agent (Master Mode) started." if enable_distributed else "Orchestration Agent (Local Mode) started.")
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
                # Monitor processes for up to 60 minutes (60 * 60 seconds)
                for _ in range(60):
                    monitor_and_restart(processes, scripts)
                    time.sleep(60)
            except KeyboardInterrupt:
                logger.info("Train phase monitoring loop interrupted. Proceeding to training process cleanup and main loop exit.")
                # When KeyboardInterrupt occurs here, we break out of the `while True` loop entirely.
                # This ensures the 'Analytics Phase' and subsequent iterations are skipped for this run.
                break
            finally:
                logger.info("--- [Halt Phase] Stopping training processes ---")
                try:
                    cleanup(processes)
                    time.sleep(2)
                except KeyboardInterrupt:
                    logger.info("Ignored extra Ctrl+C during training process cleanup. Continuing safe shutdown.")

            # These phases run only if the training loop completes its 60 iterations
            # without a KeyboardInterrupt or other exception that breaks the loop earlier.
            logger.info("--- [Analytics Phase] Running synchronous checks ---")
            from factory.log_pruner import prune_logs
            prune_logs(max_files=1000)
            
            # --- TRUE AUTOMATION: RL & EVOLUTION ---
            try:
                from factory.ppo_trainer import PPOTrainer
                logger.info("Starting automated PPO Training on collected replays...")
                trainer = PPOTrainer()
                trainer.train()
                logger.info("PPO Training complete. New weights generated.")
            except Exception as e:
                logger.error(f"Automated PPO Training failed: {e}", exc_info=True)

            try:
                from factory.teams.development_team import DevelopmentTeam
                DevelopmentTeam().run_development(iteration)
            except Exception as e:
                logger.error(f"Development Team cycle failed: {e}", exc_info=True)

            run_hourly_checks(iteration)
            run_analytics_check(iteration)
            
            if enable_distributed:
                try:
                    from factory.orchestrator_master_git import auto_commit_and_push_if_changed
                    auto_commit_and_push_if_changed()
                except Exception as e:
                    logger.error(f"Git auto-push failed: {e}")
                
            iteration += 1
    except KeyboardInterrupt:
        logger.info("Orchestration Agent (Master Mode) received KeyboardInterrupt. Initiating graceful shutdown.")
    except Exception as e:
        # Catch any other unexpected exceptions and log them with stack trace
        logger.error(f"Orchestration Agent (Master Mode) crashed due to unhandled exception: {e}", exc_info=True)
    finally:
        if beacon:
            logger.info("Stopping MasterBeacon...")
            beacon.stop()
        logger.info("Orchestration Agent (Master Mode) shutdown complete.")