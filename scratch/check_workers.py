import os
import re

log_path = "logs/master_server.log"
if os.path.exists(log_path):
    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # Look for worker registrations in the log
        registrations = re.findall(r"worker.*register|register.*worker", content, re.IGNORECASE)
        print(f"Total worker registration log entries: {len(registrations)}")
        
        # Look for unique worker connections
        worker_ids = set(re.findall(r"worker_\d+|worker-\d+", content, re.IGNORECASE))
        if worker_ids:
            print(f"Unique workers mentioned in logs: {worker_ids}")
        else:
            print("No specific worker IDs found in log patterns.")
    except Exception as e:
        print(f"Error reading master log: {e}")

# Check active python processes
print("\n=== Active Python Processes ===")
os.system("tasklist | findstr python")
