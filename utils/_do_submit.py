import json
import subprocess
import sys
from pathlib import Path


def _do_submit(api, current_best, reason):
    logger.info(f"TRIGGERING SUBMISSION: {reason}")
    try:
        subprocess.run([sys.executable, "build_submission.py"], check=True)
        desc = f"Apex Auto: Fitness {current_best:.2f}. {reason}"
        api.competition_submit("submission.tar.gz", desc, "pokemon-tcg-ai-battle")
        Path("logs/last_submitted_fitness.json").write_text(json.dumps({"last_submitted_fitness": current_best}), encoding="utf-8")
        logger.info("Submission successful.")
    except Exception as e:
        logger.error(f"Submission failed: {e}")

