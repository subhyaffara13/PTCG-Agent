import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run.deps import check_and_install_dependencies
from run.handler import log_crash

sys.excepthook = log_crash


def main():
    check_and_install_dependencies()
    print("[INFO] Starting PTCG Agent Orchestrator...")
    try:
        from factory.orchestration_agent import main as orch_main
        orch_main()
    except KeyboardInterrupt:
        print("\n[INFO] Process terminated by user (Ctrl+C). Exiting gracefully...")
        sys.exit(0)


if __name__ == "__main__":
    main()
