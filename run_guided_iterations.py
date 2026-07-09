"""
run_guided_iterations.py
Orchestrates running ptcg-agent training iterations with strategy/deck changes.
"""
import sys
import os
import json
import subprocess
from pathlib import Path
import logging

sys.path = [p for p in sys.path if "kaggle_environments" not in p]
if os.getcwd() not in sys.path: sys.path.insert(0, os.getcwd())

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("run_guided_iterations")

from run_factory import run_iteration
from run_guided_helpers import get_last_iteration_id, execute_refactor_step, execute_ppo_step

def get_archetype_for_iteration(i: int) -> str:
    if i % 100 == 0: return ["aggro", "control", "combo", "utility"][(i // 100) % 4]
    if i % 5 == 0: return ["aggro", "control", "tempo"][(i // 5) % 3]
    return "aggro"

def main():
    # Use the full MCTS + C++ + value-network pipeline during training.
    # FAST_SIM_MODE is only activated on Kaggle when the C++ extension is missing.
    os.environ.pop("FAST_SIM_MODE", None)  # ensure it is unset locally
    
    last_iter = get_last_iteration_id()
    start_iter = last_iter + 1
    num_iters = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 100
    end_iter = last_iter + num_iters
    logger.info(f"Starting fast guided iterations from {start_iter} to {end_iter} ({num_iters} iterations)")
    
    for i in range(start_iter, end_iter + 1):
        pct = (i - start_iter) / (end_iter - start_iter + 1) * 100
        forced_archetype = get_archetype_for_iteration(i)
        forced_escalation = {"deck_architect": True, "builder_agent": False} if (i % 100 == 0 or i % 10 == 0) else None
        logger.info(f"\n{'='*60}")
        logger.info(f"  ITERATION {i}  [{pct:.0f}% complete]  archetype={forced_archetype}")
        if forced_escalation:
            logger.info(f"  Escalation: {forced_escalation}")
        logger.info(f"{'='*60}")
        
        if i % 50 == 0: execute_refactor_step(i)
            
        try:
            run_iteration(iteration_id=i, forced_archetype=forced_archetype, forced_escalation=forced_escalation)
        except Exception as e:
            logger.error(f"Error during iteration {i}: {e}", exc_info=True)
            break

        orig_fast = os.environ.get("FAST_SIM_MODE")
        os.environ["FAST_SIM_MODE"] = "false"
        try:
            execute_ppo_step(i)
        finally:
            if orig_fast is not None:
                os.environ["FAST_SIM_MODE"] = orig_fast
            else:
                del os.environ["FAST_SIM_MODE"]
            
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
            try: subprocess.run([sys.executable, "build_submission.py"], check=True)
            except Exception as e: logger.error(f"Failed to auto-build submission: {e}")

if __name__ == "__main__":
    main()
