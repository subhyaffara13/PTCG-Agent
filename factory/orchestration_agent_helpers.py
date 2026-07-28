"""
factory/orchestration_agent_helpers.py
Helpers for the orchestration agent: auto-submission, analytics, script config.
"""
import sys
import json
import subprocess
import logging
from pathlib import Path

from factory.orchestration_agent_utils import get_training_scripts, read_fitness

logger = logging.getLogger("orchestration_agent")


def run_analytics_check(iteration: int):
    """Runs AnalyticsTeam on the latest iteration results."""
    try:
        from factory.teams.analytics_team import AnalyticsTeam
        result_file = Path("logs/iteration_result.json")
        if result_file.exists():
            res_data = json.loads(result_file.read_text(encoding="utf-8"))
            analytics = AnalyticsTeam()
            analytics.run_analysis(
                iteration_id=iteration, log_dir="logs",
                iteration_result=res_data, decks={"player_a": [], "player_b": []}
            )
            logger.info("Analytics heavy check finished.")
    except Exception as e:
        logger.error(f"Analytics check failed: {e}")


def auto_submit_if_ready():
    """Checks fitness, submission budget, and uploads to Kaggle if warranted."""
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        from datetime import datetime, timezone
    except ImportError:
        logger.warning("Kaggle API not available. Skipping auto-submit.")
        return

    import time
    api = None
    subs = None
    for attempt in range(3):
        try:
            api = KaggleApi()
            api.authenticate()
            subs = api.competition_submissions("pokemon-tcg-ai-battle")
            break
        except Exception as e:
            if attempt == 2:
                logger.error(f"Kaggle auth/query failed after 3 attempts: {e}")
                return
            logger.warning(f"Kaggle query failed (attempt {attempt+1}), retrying in {2**attempt}s...: {e}")
            time.sleep(2**attempt)

    if api is None or subs is None:
        return

    now_utc = datetime.now(timezone.utc)
    today_subs = sum(1 for s in subs if s is not None and s.date.replace(tzinfo=timezone.utc).date() == now_utc.date())
    last_sub_time = max((s.date.replace(tzinfo=timezone.utc) for s in subs if s is not None), default=None)
    elapsed_hours = (now_utc - last_sub_time).total_seconds() / 3600.0 if last_sub_time else 999.0

    logger.info(f"Submissions today: {today_subs}/5, hours since last: {elapsed_hours:.1f}h")

    current_best = read_fitness("logs/best_fitness.json", "best_fitness")
    last_submitted = read_fitness("logs/last_submitted_fitness.json", "last_submitted_fitness")
    is_new_best = current_best > last_submitted + 0.1

    if today_subs >= 5:
        return
    if elapsed_hours < 4.5:
        logger.info(f"Skipping auto-submit: only {elapsed_hours:.2f}h elapsed (requires 4.5h spacing).")
        return
    if is_new_best:
        reason = f"Breakthrough! {last_submitted:.2f} -> {current_best:.2f}"
    else:
        reason = f"Spacing: {elapsed_hours:.1f}h elapsed"

    try:
        from factory.gauntlet_runner import GauntletRunner
        import csv
        
        candidate_deck = []
        deck_file = Path("deck.csv")
        if deck_file.exists():
            with open(deck_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    count = int(row.get("count", 1))
                    card_id = row.get("card_id", "")
                    candidate_deck.extend([card_id] * count)
        
        if candidate_deck:
            gauntlet = GauntletRunner()
            res = gauntlet.run_gauntlet(candidate_deck, num_games_per_archetype=2)
            passed = res.get("passed", False) if isinstance(res, dict) else bool(res)
            if not passed:
                logger.info("REJECTING AUTO-SUBMIT: Failed Gauntlet gate (win rate < 50%)")
                return
    except Exception as e:
        logger.error(f"Gauntlet gate crashed, skipping: {e}")

    logger.info(f"TRIGGERING SUBMISSION: {reason}")
    try:
        subprocess.run([sys.executable, "build_submission.py"], check=True)
        desc = f"Apex Auto: Fitness {current_best:.2f}. {reason}"
        api.competition_submit("submission.tar.gz", desc, "pokemon-tcg-ai-battle")
        Path("logs/last_submitted_fitness.json").write_text(
            json.dumps({"last_submitted_fitness": current_best}), encoding="utf-8")
        logger.info("Submission successful.")
    except Exception as e:
        logger.error(f"Submission failed: {e}")
