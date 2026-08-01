"""
run_guided_iterations.py
Orchestrates running ptcg-agent training iterations with strategy/deck changes.
"""
import sys
import os
import json
import subprocess
from pathlib import Path
import logging

sys.path = [p for p in sys.path if "kaggle_environments" not in p]
if os.getcwd() not in sys.path: sys.path.insert(0, os.getcwd())

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("run_guided_iterations")

from run_factory import run_iteration
from run_guided_helpers import get_last_iteration_id, execute_refactor_step, execute_ppo_step, update_league_from_iteration

from utils.get_archetype_for_iteration import get_archetype_for_iteration

from utils.main import main

if __name__ == "__main__":
    main()
