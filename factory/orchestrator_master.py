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
    try:
        while True:
            logger.info("--- [Train Phase] Starting distributed master and PPO workers ---" if enable_distributed else "--- [Train Phase] Starting local training processes ---")
            processes = launch_processes(scripts)
            try:
                for _ in range(60):
                    monitor_and_restart(processes, scripts)
                    time.sleep(60)
            except KeyboardInterrupt:
                logger.info("Loop manually interrupted. Shutting down gracefully...")
                raise  # Re-raise to break out of the top-level while loop
            finally:
                logger.info("--- [Halt Phase] Stopping training processes ---")
                try:
                    cleanup(processes)
                    time.sleep(2)
                except KeyboardInterrupt:
                    logger.info("Ignored extra Ctrl+C. Continuing safe shutdown...")

            logger.info("--- [Analytics Phase] Running synchronous checks ---")
            from factory.log_pruner import prune_logs
            prune_logs(max_files=1000)
            run_hourly_checks(iteration)
            run_analytics_check(iteration)
            
            if enable_distributed:
                try:
                    from factory.orchestrator_master_git import auto_commit_and_push_if_changed
                    auto_commit_and_push_if_changed()
                except Exception as e:
                    logger.error(f"Git auto-push failed: {e}")
                
            iteration += 1
    except Exception as e:
        logger.error(f"Loop crashed: {e}")
    finally:
        if beacon:
            beacon.stop()
