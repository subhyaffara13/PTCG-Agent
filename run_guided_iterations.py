"""
run_guided_iterations.py

Orchestrates running ptcg-agent training iterations with the following schedule:
- Every 5 iterations: Switch strategy (alternate archetype between aggro, control, tempo).
- Every 10 iterations: Switch card deck (escalate to DeckArchitect).
- Every 50 iterations: Refactor codebase, run full tests, and rebuild submission package.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("run_guided_iterations")

from run_factory import run_iteration

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
    
    # 1. Run pytest suite to ensure code health
    logger.info("Running pytest suite...")
    try:
        res = subprocess.run(["pytest"], capture_output=True, text=True, check=True)
        logger.info(f"Pytest passed:\n{res.stdout[-500:]}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Pytest failed during refactor step!\n{e.stderr}\n{e.stdout}")
        
    # 2. Run build_submission.py to package the latest changes
    logger.info("Re-building submission package...")
    try:
        res = subprocess.run([sys.executable, "build_submission.py"], capture_output=True, text=True, check=True)
        logger.info(res.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"build_submission.py failed: {e.stderr}")

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
        
        forced_archetype = "aggro"
        forced_escalation = None
        
        # Rule 0: Every 100 iterations, force a complete deck and strategy redraw into a new archetype
        if i % 100 == 0:
            all_archetypes = ["aggro", "control", "combo", "utility"]
            idx = (i // 100) % len(all_archetypes)
            forced_archetype = all_archetypes[idx]
            logger.info(f"[MASTER ARCHETYPE SHIFT] Iteration {i} is a multiple of 100. Redrawing deck and strategy to archetype: {forced_archetype}")
            forced_escalation = {"deck_architect": True, "builder_agent": False}
        
        # Rule 1: Every 5 iterations, switch strategy (archetype)
        elif i % 5 == 0:
            archetypes = ["aggro", "control", "tempo"]
            # Alternate based on divisor
            idx = (i // 5) % len(archetypes)
            forced_archetype = archetypes[idx]
            logger.info(f"[STRATEGY SWITCH] Iteration {i} is a multiple of 5. Forcing strategy archetype: {forced_archetype}")
            
        # Rule 2: Every 10 iterations, switch card deck
        if i % 10 == 0:
            logger.info(f"[DECK SWITCH] Iteration {i} is a multiple of 10. Forcing DeckArchitect build.")
            forced_escalation = {"deck_architect": True, "builder_agent": False}
            
        # Rule 3: Every 50 iterations, run refactor and build
        if i % 50 == 0:
            logger.info(f"[REFACTOR STEP] Iteration {i} is a multiple of 50. Performing refactor and cleanup before running games.")
            execute_refactor_step(i)
            
        # Run the iteration with forced parameters
        try:
            run_iteration(
                iteration_id=i,
                forced_archetype=forced_archetype,
                forced_escalation=forced_escalation
            )
        except Exception as e:
            logger.error(f"Error during iteration {i}: {e}", exc_info=True)
            break
            
        # Sync and compile the latest submission code only when the score improved or at the final round
        should_build = (i == end_iter)
        eval_report_path = Path("eval_report.json")
        if eval_report_path.exists():
            try:
                report_data = json.loads(eval_report_path.read_text(encoding="utf-8"))
                best_ver = report_data.get("version_scores", {}).get("best_version", "player_a")
                if best_ver == "player_b":
                    should_build = True
                    logger.info(f"Iteration {i} achieved a new high score! Triggering build.")
            except Exception as e:
                logger.warning(f"Could not read eval_report.json to determine build need: {e}")

        if should_build:
            logger.info("Building latest submission tarball...")
            try:
                subprocess.run([sys.executable, "build_submission.py"], check=True)
            except Exception as e:
                logger.error(f"Failed to auto-build submission: {e}")
        else:
            logger.info(f"Skipping build for iteration {i} (no score improvement).")

if __name__ == "__main__":
    # Allow running a dry-run to verify scheduling
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        last_iter = 90
        logger.info("--- DRY RUN SCHEDULING VERIFICATION ---")
        for i in range(last_iter + 1, last_iter + 21):
            sched_info = []
            if i % 5 == 0:
                idx = (i // 5) % 3
                sched_info.append(f"Strategy Switch (archetype: {['aggro', 'control', 'tempo'][idx]})")
            if i % 10 == 0:
                sched_info.append("Deck Switch (DeckArchitect)")
            if i % 50 == 0:
                sched_info.append("Refactor Step")
            
            if sched_info:
                logger.info(f"Iteration {i}: {', '.join(sched_info)}")
            else:
                logger.info(f"Iteration {i}: Normal weight tuning")
    else:
        main()
