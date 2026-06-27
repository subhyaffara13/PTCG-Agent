"""
scratch/run_ppo_update.py
Decoupled PPO update runner, invoked via subprocess to avoid stale code.
"""
import os
import sys
from pathlib import Path

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

from run_guided_helpers import execute_ppo_step, get_last_iteration_id

def main():
    orig = os.environ.get("FAST_SIM_MODE")
    os.environ["FAST_SIM_MODE"] = "false"
    try:
        execute_ppo_step(get_last_iteration_id())
    except Exception as e:
        print(f"PPO training failed: {e}")
    finally:
        if orig is not None:
            os.environ["FAST_SIM_MODE"] = orig
        else:
            os.environ.pop("FAST_SIM_MODE", None)

if __name__ == "__main__":
    main()
