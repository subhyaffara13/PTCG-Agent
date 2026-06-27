import json
import logging
from pathlib import Path

from scratch.hourly_audit_checks import check_file_limits, check_online_submissions
from scratch.hourly_audit_report import run_cmd

logger = logging.getLogger(__name__)


def main():
    print("==================================================")
    print("HOURLY AUDIT REPORT")
    print("==================================================")
    run_cmd("python scratch/run_leaderboard_loop.py")
    check_online_submissions()
    iter_file = Path("logs/iteration_result.json")
    if iter_file.exists():
        try:
            data = json.loads(iter_file.read_text(encoding="utf-8"))
            print(f"\n--- MATCH HISTORY (Iteration {data.get('iteration')}) ---")
            for k, g in data.get("games", {}).items():
                print(f"  {k}: Winner = {g.get('winner')}, Turns = {g.get('turns_taken')}")
        except Exception as e:
            print(f"Failed to read iteration result: {e}")
    check_file_limits()
    run_cmd("python build_submission.py")
    print("==================================================")


if __name__ == "__main__":
    main()


__all__ = [
    "run_cmd", "check_file_limits", "download_and_analyze_my_replays",
    "check_online_submissions", "main",
]
