"""
scratch/run_active_evolution.py
Active evolutionary heuristics optimization loop.
"""
import sys
import os
from dotenv import load_dotenv
load_dotenv()

import json
import shutil
import time
import subprocess
from pathlib import Path

# Setup project root path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - ActiveEvolve - %(levelname)s - %(message)s")
logger = logging.getLogger("active_evolution")

from cb_agents.code_mutator import request_code_mutation_from_llm, push_mutation_to_git
from factory.gauntlet_runner import GauntletRunner
from factory.game_runner import DEFAULT_DECK

def evaluate_heuristics(num_games: int = 2) -> float:
    """Run the gauntlet evaluation and return the overall win rate."""
    try:
        runner = GauntletRunner()
        # Evaluate against the 4 key gauntlet archetypes
        win_rate = runner.run_gauntlet(DEFAULT_DECK, num_games_per_archetype=num_games)
        return float(win_rate)
    except Exception as e:
        logger.error(f"Gauntlet evaluation failed: {e}")
        return 0.0

def main():
    target_file = "cb_agents/turn_planner_sort.py"
    file_path = PROJECT_ROOT / target_file
    if not file_path.exists():
        logger.error(f"Target file {file_path} not found.")
        sys.exit(1)

    logger.info("Step 1: Running baseline gauntlet evaluation...")
    baseline_win_rate = evaluate_heuristics(num_games=2)
    logger.info(f"Baseline Win Rate: {baseline_win_rate * 100:.1f}%")

    logger.info("Step 2: Requesting optimistic heuristic mutations from LLM...")
    feedback = f"""
    The current heuristics in turn_planner_sort.py achieved a win rate indicator of {baseline_win_rate*100:.1f}%.
    We are targeting an Elite Grandmaster Elo rating of 1300+ on the leaderboard.
    A score below 600 is completely unacceptable and indicates poor reasoning, misplayed cards, or a broken strategy.
    We need at least 1000 to enter the leaderboard, and are aiming for 1300.
    
    Optimistically rewrite and optimize the priorities in sort_actions_heuristically() to increase this win rate:
    - Never make unnecessary passes or pass turns when attacks are available.
    - Plan multi-turn setups. Prioritize benching core attackers, attaching energy to the correct active/bench targets based on preference mappings.
    - Play high-value trainers (e.g., search/draw cards) early in the turn to expand options before choosing energy targets or attacking.
    - Ensure perfect syntax, no type mismatches, and avoid PEP 701 f-string nested quotes.
    
    CRITICAL RESTRICTION: DO NOT delete any existing rules, helper functions, or core logic unless you are specifically rewriting them to be strictly better. Do not truncate the file. If you delete random code, the agent will crash and lose the game.
    """
    
    mutated_code = request_code_mutation_from_llm(file_path, feedback)
    if not mutated_code:
        logger.error("Failed to fetch mutation from LLM.")
        sys.exit(1)

    logger.info("Step 3: Creating timestamped backup in .history directory...")
    history_dir = PROJECT_ROOT / ".history"
    history_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_path = history_dir / f"{file_path.stem}_{timestamp}.py.bak"
    shutil.copy2(file_path, backup_path)
    logger.info(f"Backup saved to: {backup_path}. You can revert to this file at any time.")

    try:
        # Apply mutation
        file_path.write_text(mutated_code, encoding="utf-8")
        logger.info("Applied mutation. Running pytest guardrails...")

        # Run pytest
        test_res = subprocess.run(["pytest"], capture_output=True, text=True)
        if test_res.returncode != 0:
            raise Exception(f"Pytest suite failed: {test_res.stdout[-1000:]}")
        logger.info("Pytest guardrails passed.")

        # Re-evaluate mutated code
        logger.info("Step 4: Running mutated gauntlet evaluation...")
        mutated_win_rate = evaluate_heuristics(num_games=2)
        
        # Estimate Elo based on gauntlet indicator
        est_elo = 400 + (mutated_win_rate * 80)
        logger.info(f"Mutated Win Rate Indicator: {mutated_win_rate * 100:.1f}% (Baseline: {baseline_win_rate * 100:.1f}%)")
        logger.info(f"Estimated Agent Elo: {est_elo:.0f} (Milestones: 600 Baseline, 1000 Leaderboard, 1300 Target)")

        if est_elo < 600:
            logger.warning(f"Rejecting mutation: Estimated Elo ({est_elo:.0f}) is below the required 600 baseline milestone!")
            shutil.move(backup_path, file_path)
            sys.exit(0)

        # Promote if it improves performance (win rate increases or is equal to baseline if win rate was high)
        if mutated_win_rate > baseline_win_rate or (mutated_win_rate == baseline_win_rate and baseline_win_rate >= 0.70):
            logger.info("Mutated heuristics OUTPERFORMED or MATCHED baseline. Promoting and pushing...")
            backup_path.unlink()
            
            # Commit and push
            push_mutation_to_git(file_path, f"Optimized heuristics from {baseline_win_rate*100:.1f}% to {mutated_win_rate*100:.1f}% indicator (Estimated Elo: {est_elo:.0f})")
            logger.info("Mutation promoted successfully!")
        else:
            logger.info("Mutation did not improve performance. Rolling back...")
            shutil.move(backup_path, file_path)
            
    except Exception as e:
        logger.error(f"Mutation rejected during active evolution: {e}")
        if backup_path.exists():
            logger.info("Restoring original code...")
            shutil.move(backup_path, file_path)

if __name__ == "__main__":
    main()
