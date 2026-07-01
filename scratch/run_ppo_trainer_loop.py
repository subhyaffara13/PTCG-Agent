import sys
import os
import time

# Ensure root folder is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scratch.run_ppo_trainer_loop_parts import process_if_changed, TELEMETRY_PATH

POLL_INTERVAL_SECONDS = 5.0

def main():
    print("Starting Decoupled PPO Trainer Loop with Polling...")
    print(f"Polling {TELEMETRY_PATH} every {POLL_INTERVAL_SECONDS} seconds.")
    
    last_mtime = 0.0
    while True:
        try:
            last_mtime = process_if_changed(last_mtime)
        except Exception as e:
            print(f"Error in PPO loop: {e}")
        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
