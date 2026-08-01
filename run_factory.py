"""
run_factory.py

Team-Based Multi-Agent Pipeline
Orchestrates parallel execution of agent teams to ensure stability and speed.
"""

import sys
import json
import logging
from pathlib import Path

from run_factory_utils import run_team_pipeline as _run_team_pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

from utils.run_team_pipeline import run_team_pipeline

run_iteration = run_team_pipeline

import signal
import os

from utils._instant_signal_handler import _instant_signal_handler

signal.signal(signal.SIGINT, _instant_signal_handler)

if __name__ == "__main__":
    start_iter = 1
    try:
        report_path = Path("logs/eval_report.json")
        if report_path.exists():
            data = json.loads(report_path.read_text(encoding="utf-8"))
            start_iter = data.get("iteration", 0) + 1
    except Exception:
        pass
    iterations_to_run = 1
    if len(sys.argv) > 1:
        iterations_to_run = int(sys.argv[1])
    for i in range(start_iter, start_iter + iterations_to_run):
        run_team_pipeline(i)
