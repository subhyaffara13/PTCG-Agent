import sys
import os

log_path = "logs/master_server.log"
if not os.path.exists(log_path):
    print(f"Log file {log_path} does not exist.")
    sys.exit(0)

try:
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        # Seek near the end of the file
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        # Read the last 50KB of data
        seek_pos = max(0, file_size - 50000)
        f.seek(seek_pos)
        lines = f.readlines()
        
        # Show the last 100 lines
        print(f"=== Last 100 lines of {log_path} ===")
        for line in lines[-100:]:
            print(line, end="")
except Exception as e:
    print(f"Error reading log file: {e}")
