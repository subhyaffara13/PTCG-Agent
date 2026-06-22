import os
import sys
import time
from pathlib import Path

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

from run_guided_helpers import execute_ppo_step

def main():
    print("Starting Decoupled PPO Trainer Loop...")
    last_mod = 0.0
    telemetry_path = Path("logs/iteration_result.json")
    
    while True:
        current_mod = telemetry_path.stat().st_mtime if telemetry_path.exists() else 0.0
        if current_mod != last_mod:
            print("New iteration telemetry detected! Training policy network in the background...")
            orig = os.environ.get("FAST_SIM_MODE")
            os.environ["FAST_SIM_MODE"] = "false"
            try:
                from run_guided_helpers import get_last_iteration_id
                iter_id = get_last_iteration_id()
                execute_ppo_step(iter_id)
                last_mod = current_mod
            except Exception as e:
                print(f"PPO training failed: {e}")
            if orig is not None:
                os.environ["FAST_SIM_MODE"] = orig
            else:
                del os.environ["FAST_SIM_MODE"]
        time.sleep(15)

if __name__ == "__main__":
    main()
