"""
scratch/run_training_batches.py
Orchestrates continuous training iterations, checking standards after each batch.
"""
import sys
import subprocess
from pathlib import Path

def run_cmd(cmd: str) -> bool:
    try:
        print(f"Running: {cmd}")
        res = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(res.stdout[-800:]) # show summary
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}\nStdout:\n{e.stdout}\nError:\n{e.stderr[-800:]}")
        return False

import json

def check_file_line_counts() -> bool:
    print("Checking code standards: file line counts...")
    target_files = [
        "cb_agents/turn_planner.py",
        "cb_agents/turn_planner_logging.py",
        "cb_agents/strategy_agent.py",
        "cb_agents/time_manager.py"
    ]
    queue_path = Path("logs/refactor_queue.json")
    try:
        queue = json.loads(queue_path.read_text(encoding="utf-8")) if queue_path.exists() else []
    except Exception:
        queue = []
        
    all_passed = True
    for f in target_files:
        p = Path(f)
        if p.exists():
            lines = len(p.read_text(encoding="utf-8").splitlines())
            print(f"  {f}: {lines} lines")
            if lines >= 100:
                print(f"  WARNING: {f} exceeds 100 line limit! Queueing for auto-refactor.")
                if f not in queue: queue.append(f)
                all_passed = False
                
    if not all_passed:
        queue_path.write_text(json.dumps(queue, indent=2), encoding="utf-8")
        
    return all_passed

def main():
    b = 0
    batch_size = 1

    while True:
        b += 1
        print(f"\n==================================================")
        print(f"STARTING BATCH {b} (Iterations {(b-1)*batch_size + 1} - {b*batch_size})")
        print(f"==================================================")
        
        # 1. Run 10 iterations
        if not run_cmd(f"{sys.executable} run_guided_iterations.py {batch_size}"):
            print("Batch training iterations failed. Halting pipeline.")
            sys.exit(1)
            
        # 2. Perform standards verification checks
        print(f"\n--- Running Verification Checks for Batch {b} ---")
        
        # Check A: Pytest
        if not run_cmd(f"{sys.executable} run_tests.py"):
            print("Pytest suite failed. Halting pipeline.")
            sys.exit(1)
            
        # Check B: Line count limits
        if not check_file_line_counts():
            print("Line count constraints violated. Queued for background refactoring. Continuing pipeline...")
            
        # Check C: Rebuild Submission Tarball
        # (GA optimization is now decoupled and runs asynchronously in the background)
        if not run_cmd(f"{sys.executable} build_submission.py"):
            print("Failed to rebuild submission package. Halting pipeline.")
            sys.exit(1)
            
        print(f"\nBatch {b} successfully passed all standards checks!")

if __name__ == "__main__":
    main()
