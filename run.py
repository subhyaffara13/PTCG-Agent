"""
PTCG Agent Top-level Entrypoint.
Simplifies running the orchestration agent or master loop across all machines.

Usage:
  python run.py                <- Starts in auto-discovery mode (worker/master auto-election)
  python run.py --force master <- Force starts this machine as the Master server
"""
import sys
import os

import traceback
import datetime

def log_crash(exctype, value, tb):
    # Print to console standard stderr
    sys.__excepthook__(exctype, value, tb)
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/crash_report.log", "a", encoding="utf-8") as f:
            f.write(f"\n--- CRASH REPORT AT {datetime.datetime.now()} ---\n")
            traceback.print_exception(exctype, value, tb, file=f)
    except Exception:
        pass

sys.excepthook = log_crash

def check_and_install_dependencies():
    print("[INFO] Checking dependencies...")
    import subprocess
    from pathlib import Path
    req_file = Path(__file__).parent / "requirements.txt"
    if not req_file.exists():
        print("[WARNING] requirements.txt not found. Skipping dependency check.")
        return
        
    try:
        import importlib.metadata
        import re
        requirements = req_file.read_text(encoding="utf-8").splitlines()
        requirements = [r.strip() for r in requirements if r.strip() and not r.startswith("#")]
        for req in requirements:
            package_name = re.split(r'[><=!~;\[]', req)[0].strip()
            # Try to fetch version to check if installed
            importlib.metadata.version(package_name)
        print("[INFO] All dependencies satisfied.")
        return
    except Exception:
        pass
        
    print("[INFO] Installing/updating missing dependencies from requirements.txt...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
            check=True
        )
        print("[INFO] Dependencies successfully installed.")
    except Exception as e:
        print(f"[ERROR] Failed to install dependencies: {e}")

if __name__ == "__main__":
    # Ensure current directory is in path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    check_and_install_dependencies()
    print("[INFO] Starting PTCG Agent Orchestrator...")
    
    try:
        # Forward arguments and call orchestration_agent main
        from factory.orchestration_agent import main
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Process terminated by user (Ctrl+C). Exiting gracefully...")
        sys.exit(0)
