import os
import glob

def check_file(filename, tail_lines=2000):
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()[-tail_lines:]
            
        errors = []
        for i, line in enumerate(lines):
            if 'Traceback' in line or 'Error' in line or 'Exception' in line:
                errors.append(line.strip())
        
        if errors:
            print(f"\n=== Errors in {filename} ===")
            for err in set(errors[-20:]):  # Deduplicate and show last 20
                print(err)
    except Exception as e:
        print(f"Could not read {filename}: {e}")

if __name__ == "__main__":
    logs = [
        "logs/run_deck_optimizer_loop.log",
        "logs/run_ppo_trainer_loop.log",
        "logs/run_training_batches.log",
        "logs/master_server.log",
        "logs/crash_report.log"
    ]
    for log in logs:
        check_file(log)
