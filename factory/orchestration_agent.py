"""
factory/orchestration_agent.py
Top-level orchestration loop: launches training, monitors health, auto-submits.
"""
import sys
import os
import time
import subprocess
import json
import logging
from factory.orchestration_agent_helpers import (
    auto_submit_if_ready, run_analytics_check, get_training_scripts
)
from factory.orchestration_process import (
    launch_processes, monitor_and_restart, cleanup, script_log_path
)

os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("orchestration_agent")
logger.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

fh = logging.FileHandler("logs/orchestration_agent.log", mode="a", encoding="utf-8")
fh.setFormatter(fmt)
logger.addHandler(fh)

sh = logging.StreamHandler()
sh.setFormatter(fmt)
logger.addHandler(sh)

ENABLE_DISTRIBUTED = True


def run_hourly_checks(iteration: int):
    """Runs leaderboard checks and auto-submission logic."""
    logger.info(f"--- [Orchestration] Hourly check #{iteration} ---")
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


def main():
    logger.info("Orchestration Agent started (Block-Synchronous).")
    scripts = get_training_scripts(ENABLE_DISTRIBUTED)

    iteration = 0
    while True:
        logger.info("--- [Train Phase] Starting training workers ---")
        processes = launch_processes(scripts)
        try:
            for _ in range(60):
                monitor_and_restart(processes, scripts)
                time.sleep(60)
        finally:
            logger.info("--- [Halt Phase] Stopping workers for analytics ---")
            cleanup(processes)
            time.sleep(5)

        logger.info("--- [Analytics Phase] Running synchronous checks ---")
        from factory.log_pruner import prune_logs
        prune_logs(max_files=1000)
        run_hourly_checks(iteration)
        run_analytics_check(iteration)

        iteration += 1

if __name__ == "__main__":
    main()
