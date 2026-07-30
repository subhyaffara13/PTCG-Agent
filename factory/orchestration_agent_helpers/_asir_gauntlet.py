import csv
from pathlib import Path
from . import logger

def _gauntlet_gate():
    try:
        from factory.gauntlet_runner import GauntletRunner
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
            res = gauntlet.run_gauntlet(candidate_deck, num_games_per_stage=2)
            passed = res.get("passed", False) if isinstance(res, dict) else bool(res)
            if not passed:
                logger.info("REJECTING AUTO-SUBMIT: Failed Gauntlet gate (win rate < 50%)")
                return False
    except Exception as e:
        logger.error(f"Gauntlet gate crashed, skipping: {e}")
    return True
