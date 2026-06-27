import sys
import json
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger("run_guided_helpers")

def get_last_iteration_id() -> int:
    eval_report = Path("logs/eval_report.json")
    if eval_report.exists():
        try:
            data = json.loads(eval_report.read_text(encoding="utf-8"))
            if data is None:
                data = {}
            return int(data.get("iteration", 90))
        except Exception as e:
            logger.warning(f"Failed to read iteration ID from eval_report: {e}")
    return 90

def execute_refactor_step(iteration_id: int):
    logger.info(f"=== ITERATION {iteration_id}: INITIATING REFACTOR/CLEANUP STEP ===")
    logger.info("Running pytest suite...")
    try:
        res = subprocess.run(["pytest"], capture_output=True, text=True, check=True)
        logger.info(f"Pytest passed:\n{res.stdout[-500:]}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Pytest failed during refactor step!\n{e.stderr}\n{e.stdout}")
    logger.info("Re-building submission package...")
    try:
        res = subprocess.run([sys.executable, "build_submission.py"], capture_output=True, text=True, check=True)
        logger.info(res.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"build_submission.py failed: {e.stderr}")
