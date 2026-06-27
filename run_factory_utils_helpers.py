"""
run_factory_utils_helpers.py
----------------------------
Helper functions extracted from run_factory_utils.py.
"""

import json
import logging
from pathlib import Path
from factory.teams.analytics_team import AnalyticsTeam
from factory.teams.meta_team import MetaTeam
from factory.teams.development_team import DevelopmentTeam
from factory.teams.qa_team import QATeam
from factory.game_runner import GameRunner, DEFAULT_DECK
from factory.trajectory_logger import TrajectoryLogger

logger = logging.getLogger("run_factory")

def run_team_pipeline(iteration_id: int, forced_archetype: str = None, forced_escalation: dict = None):
    logger.info(f"=== STARTING ITERATION {iteration_id} (TEAM-BASED) ===")

    analytics_team = AnalyticsTeam()
    meta_team = MetaTeam()
    dev_team = DevelopmentTeam()
    qa_team = QATeam()

    logger.info("Phase 0: Running live game simulations...")
    runner = GameRunner()
    traj_logger = TrajectoryLogger()

    iteration_result = runner.run_iteration(
        iteration_id=iteration_id,
        version_n1=f"base_v{iteration_id}",
        version_n2=f"new_v{iteration_id}",
        deck_base=DEFAULT_DECK,
        deck_new=DEFAULT_DECK,
        reasoning_base={},
        reasoning_new={}
    )

    for label, game in iteration_result.get("games", {}).items():
        traj_logger.log_match({
            "iteration": iteration_id,
            "label": label,
            "winner": game.get("winner"),
            "turns": game.get("turns_taken", 0)
        })
    traj_logger.flush()

    logger.info("Phase 1: Analytics and Meta Analysis...")
    meta_report = meta_team.analyze_meta()

    try:
        from factory.teams.leaderboard_team import LeaderboardTeam
        leaderboard_team = LeaderboardTeam()
        leaderboard_results = leaderboard_team.run_leaderboard_feedback_loop()
        logger.info(f"Leaderboard feedback loop results: {leaderboard_results}")
    except Exception as e:
        logger.error(f"Failed to run leaderboard feedback loop: {e}")

    decks = {"player_a": DEFAULT_DECK, "player_b": DEFAULT_DECK}
    analytics_report = analytics_team.run_analysis(
        iteration_id=iteration_id, log_dir="logs",
        iteration_result=iteration_result, decks=decks
    )
    analytics_report["meta_data"] = meta_report

    logger.info("Phase 2: Development...")
    dev_results = dev_team.run_development(analytics_report)
    deck_candidate = dev_results.get("deck_candidate")
    logic_candidate = dev_results.get("logic_candidate")

    if deck_candidate or logic_candidate:
        logger.info(f"Phase 3: QA and Peer Review for candidates -> Deck: {bool(deck_candidate)}, Logic: {bool(logic_candidate)}")
        staged_deck = str(Path("staging") / "deck_new.csv") if deck_candidate else None
        staged_logic = str(Path("staging") / "logic_new.py") if logic_candidate else None
        is_approved = qa_team.run_qa_pipeline(deck_candidate=staged_deck, logic_candidate=staged_logic)
        if is_approved:
            logger.info(f"Iteration {iteration_id} completed successfully. Changes merged to baseline.")
        else:
            logger.warning(f"Iteration {iteration_id} completed. Pull Request REJECTED by QA team.")
    else:
        logger.info(f"Iteration {iteration_id} completed. Development team proposed no changes.")

    try:
        from factory.eval_agent import EvalAgent
        evaluator = EvalAgent()
        evaluator.evaluate(iteration_result)
        logger.info(f"Successfully evaluated iteration {iteration_id} and updated eval_report.json")
    except Exception as e:
        logger.error(f"Failed to run evaluation for iteration {iteration_id}: {e}")

    logger.info(f"=== COMPLETED ITERATION {iteration_id} ===\n")
    return iteration_result
