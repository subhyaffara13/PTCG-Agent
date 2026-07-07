"""
PTCG Agent Top-level Entrypoint.
Simplifies running the orchestration agent or master loop across all machines.

Usage:
  python run.py                <- Starts in auto-discovery mode (worker/master auto-election)
  python run.py --force master <- Force starts this machine as the Master server
"""
import sys
import os

import traceback
import datetime

def log_crash(exctype, value, tb):
    # Print to console standard stderr
    sys.__excepthook__(exctype, value, tb)
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/crash_report.log", "a", encoding="utf-8") as f:
            f.write(f"\n--- CRASH REPORT AT {datetime.datetime.now()} ---\n")
            traceback.print_exception(exctype, value, tb, file=f)
    except Exception:
        pass

sys.excepthook = log_crash

if __name__ == "__main__":
    # Ensure current directory is in path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    try:
        # Forward arguments and call orchestration_agent main
        from factory.orchestration_agent import main
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Process terminated by user (Ctrl+C). Exiting gracefully...")
        sys.exit(0)
