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

def run_master_loop():
    logger.info("Orchestration Agent (Master Mode) started.")
    version = get_local_version() or "unknown"
    beacon = MasterBeacon(code_version=version)
    beacon.start()
    
    scripts = get_training_scripts(enable_distributed=True)
    iteration = 0
    try:
        while True:
            logger.info("--- [Train Phase] Starting distributed master and PPO workers ---")
            processes = launch_processes(scripts)
            try:
                for _ in range(60):
                    monitor_and_restart(processes, scripts)
                    time.sleep(60)
            finally:
                logger.info("--- [Halt Phase] Stopping master server to run analytics ---")
                cleanup(processes)
                time.sleep(5)

            logger.info("--- [Analytics Phase] Running synchronous checks ---")
            from factory.log_pruner import prune_logs
            prune_logs(max_files=1000)
            run_hourly_checks(iteration)
            run_analytics_check(iteration)
            iteration += 1
    except Exception as e:
        logger.error(f"Master loop crashed: {e}")
    finally:
        beacon.stop()
