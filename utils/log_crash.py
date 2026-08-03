import os
import sys

def log_crash(exctype, value, tb):
    sys.__excepthook__(exctype, value, tb)
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/crash_report.log", "a", encoding="utf-8") as f:
            f.write(f"\n--- CRASH REPORT AT {datetime.datetime.now()} ---\n")
            traceback.print_exception(exctype, value, tb, file=f)
    except Exception:
        pass

