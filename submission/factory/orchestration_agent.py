"""
factory/orchestration_agent.py
Top-level orchestration loop: launches training, monitors health, auto-submits.
"""
import sys
import os

# Fix path for os.execv restarts which launch as script instead of module
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import time
import subprocess
import json
import logging
from factory.orchestration_agent_helpers import (
    auto_submit_if_ready, run_analytics_check, get_training_scripts
)
from factory.orchestration_process import (
    launch_processes, monitor_and_restart, cleanup, script_log_path
)

os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("orchestration_agent")
logger.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

fh = logging.FileHandler("logs/orchestration_agent.log", mode="a", encoding="utf-8")
fh.setFormatter(fmt)
logger.addHandler(fh)

sh = logging.StreamHandler()
sh.setFormatter(fmt)
logger.addHandler(sh)

from utils.main import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Agent fully terminated by user.")
        import sys
        sys.exit(0)
