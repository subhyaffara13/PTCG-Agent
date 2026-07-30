import sys
import os
import time
import subprocess
import logging
from pathlib import Path
logger = logging.getLogger(__name__)
_PRUNNABLE_PREFIXES = ("action_game_", "reasoning_game_", "steps_", "variance_game_")
_PRUNNABLE_DIRS = ("deck_test_", "opt_val_", "variance_baseline_", "reasoning_test_", "player_")
_KEEP_FILES = {"orchestration_agent.log", "crash_report.log", "iteration_result.json",
               "eval_report.json", "eval_state.json", "action_log.json", "reasoning_log.json",
               "master_server.log", "check_submissions.log", "best_fitness.json"}
_LOG_RETENTION_DAYS = 3

from .prune_old_logs import prune_old_logs
from .process_monitor import script_log_path
from .process_monitor import launch_processes
from .process_monitor import monitor_and_restart
from .cleanup import cleanup
