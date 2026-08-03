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
from run_guided_helpers import get_last_iteration_id, execute_refactor_step, execute_ppo_step, update_league_from_iteration

from utils.get_archetype_for_iteration import get_archetype_for_iteration

def main():
    os.environ.pop("FAST_SIM_MODE", None)
    
    last_iter = get_last_iteration_id()
    start_iter = last_iter + 1
    num_iters = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 100
    end_iter = last_iter + num_iters
    logger.info(f"Starting fast guided iterations from {start_iter} to {end_iter} ({num_iters} iterations)")
    
    for i in range(start_iter, end_iter + 1):
        pct = (i - start_iter) / (end_iter - start_iter + 1) * 100
        forced_archetype = get_archetype_for_iteration(i)
        forced_escalation = {"deck_architect": True, "builder_agent": False} if (i % 100 == 0 or i % 10 == 0) else None
        logger.info("\n" + "=" * 60)
        logger.info(f"Iteration {i} ({pct:.1f}% of target {end_iter})")
        logger.info(f"Active Meta: {forced_archetype or 'Auto'} | Target: {forced_escalation or 'Auto'}")
        
        run_iteration(i, forced_archetype=forced_archetype, forced_escalation=forced_escalation)
        logger.info("-" * 60)
        
        execute_refactor_step(i)
        update_league_from_iteration(i)

if __name__ == "__main__":
    main()
