"""
run_guided_iterations.py

Orchestrates running ptcg-agent training iterations with strategy/deck changes.
"""

import sys
import os

# Clean up sys.path to prevent kaggle_environments path pollution from breaking imports
sys.path = [p for p in sys.path if "kaggle_environments" not in p]
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

import json
import subprocess
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("run_guided_iterations")

from run_factory import run_iteration
from run_guided_helpers import (
    get_last_iteration_id,
    execute_refactor_step,
    execute_ppo_step,
)


def get_archetype_for_iteration(i: int) -> str:
    if i % 100 == 0:
        all_archetypes = ["aggro", "control", "combo", "utility"]
        return all_archetypes[(i // 100) % len(all_archetypes)]
    elif i % 5 == 0:
        archetypes = ["aggro", "control", "tempo"]
        return archetypes[(i // 5) % len(archetypes)]
    return "aggro"


def main():
    last_iter = get_last_iteration_id()
    start_iter = last_iter + 1
    
    num_iters = 100
    if len(sys.argv) > 1:
        try:
            num_iters = int(sys.argv[1])
        except ValueError:
            pass
            
    end_iter = last_iter + num_iters
    logger.info(f"Starting guided iterations from {start_iter} to {end_iter} ({num_iters} iterations)")
    
    for i in range(start_iter, end_iter + 1):
        logger.info(f"\n--- GUIDED ITERATION {i} ---")
        
        forced_archetype = get_archetype_for_iteration(i)
        forced_escalation = None
        
        if i % 100 == 0 or i % 10 == 0:
            logger.info(f"Forcing DeckArchitect build at iteration {i}")
            forced_escalation = {"deck_architect": True, "builder_agent": False}
        
        if i % 50 == 0:
            execute_refactor_step(i)
            
        try:
            run_iteration(
                iteration_id=i,
                forced_archetype=forced_archetype,
                forced_escalation=forced_escalation
            )
        except Exception as e:
            logger.error(f"Error during iteration {i}: {e}", exc_info=True)
            break
            
        execute_ppo_step(i)
            
        should_build = (i == end_iter)
        eval_report_path = Path("eval_report.json")
        if eval_report_path.exists():
            try:
                report_data = json.loads(eval_report_path.read_text(encoding="utf-8"))
                if report_data.get("version_scores", {}).get("best_version", "player_a") == "player_b":
                    should_build = True
                    logger.info(f"Iteration {i} achieved a new high score! Triggering build.")
            except Exception as e:
                logger.warning(f"Could not read eval_report.json: {e}")

        if should_build:
            logger.info("Building latest submission tarball...")
            try:
                subprocess.run([sys.executable, "build_submission.py"], check=True)
            except Exception as e:
                logger.error(f"Failed to auto-build submission: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        last_iter = 90
        logger.info("--- DRY RUN SCHEDULING VERIFICATION ---")
        for i in range(last_iter + 1, last_iter + 21):
            sched = []
            if i % 5 == 0:
                sched.append(f"Strategy Switch ({get_archetype_for_iteration(i)})")
            if i % 10 == 0:
                sched.append("Deck Switch (DeckArchitect)")
            if i % 50 == 0:
                sched.append("Refactor Step")
            logger.info(f"Iteration {i}: {', '.join(sched) if sched else 'Normal weight tuning'}")
    else:
        main()
