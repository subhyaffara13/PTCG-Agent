"""Helper functions extracted from run_ppo_trainer_loop.py."""

import sys
import time
import subprocess
from pathlib import Path

TELEMETRY_PATH = Path("logs/iteration_result.json")
DEBOUNCE_SECONDS = 0.25


def run_ppo_update():
    print("New iteration telemetry detected! Training policy network in the background...")
    try:
        subprocess.run([sys.executable, "-m", "factory.ppo_trainer"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"PPO training failed: {e}")


def wait_for_stable_write(path: Path) -> float:
    last_mtime = path.stat().st_mtime
    while True:
        time.sleep(DEBOUNCE_SECONDS)
        current_mtime = path.stat().st_mtime
        if current_mtime == last_mtime:
            return current_mtime
        last_mtime = current_mtime


def process_if_changed(last_mtime: float) -> float:
    if not TELEMETRY_PATH.exists():
        return last_mtime

    current_mtime = TELEMETRY_PATH.stat().st_mtime
    if current_mtime == last_mtime:
        return last_mtime

    stable_mtime = wait_for_stable_write(TELEMETRY_PATH)
    if stable_mtime != last_mtime:
        run_ppo_update()
    return stable_mtime
