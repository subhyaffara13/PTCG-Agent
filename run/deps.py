import sys
import subprocess
import importlib.metadata
import re
from pathlib import Path

def check_and_install_dependencies():
    print("[INFO] Checking dependencies...")
    req_file = Path(__file__).resolve().parent.parent / "requirements.txt"
    if not req_file.exists():
        print("[WARNING] requirements.txt not found. Skipping dependency check.")
        return
    try:
        requirements = req_file.read_text(encoding="utf-8").splitlines()
        requirements = [r.strip() for r in requirements if r.strip() and not r.startswith("#")]
        for req in requirements:
            package_name = re.split(r'[><=!~;\[]', req)[0].strip()
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
