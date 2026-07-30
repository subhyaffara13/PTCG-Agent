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

def run_team_pipeline(iteration_id: int, forced_archetype: str | None = None, forced_escalation: dict | None = None):
    return _run_team_pipeline(iteration_id, forced_archetype=forced_archetype, forced_escalation=forced_escalation)

run_iteration = run_team_pipeline

import signal
import os

def _instant_signal_handler(sig, frame):
    logging.info("Ctrl+C received. Terminating immediately...")
    os._exit(0)

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
