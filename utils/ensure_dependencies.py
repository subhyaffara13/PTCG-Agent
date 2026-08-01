import os
import sys
import time
import pathlib
import subprocess
from utils.silence_kaggle_warnings import silence_kaggle_warnings

def ensure_dependencies():
    # Purge any old colliding test_agents compiled bytecode cache files in root folder
    try:
        root_dir = pathlib.Path(__file__).parent.parent.resolve()
        for p in root_dir.glob("__pycache__/test_agents*"):
            if p.is_file():
                p.unlink()
        for p in root_dir.glob("test_agents*"):
            if p.is_file() and p.suffix in (".pyc", ".pyo"):
                p.unlink()
    except Exception:
        pass

    required_packages = ["numpy", "pydantic", "pokerkit", "dotenv", "kaggle_environments"]
    missing = False
    for pkg in required_packages:
        try:
            if pkg == "dotenv":
                import dotenv
            else:
                with silence_kaggle_warnings():
                    __import__(pkg)
        except ImportError:
            missing = True
            break
            
    if missing:
        print("Missing dependencies detected. Satisfying requirements...")
        try:
            print("Installing kaggle-environments without dependencies (avoids compiling pygame)...")
            subprocess.run([sys.executable, "-m", "pip", "install", "kaggle-environments", "--no-deps"], check=True)
            
            req_path = os.path.join(os.getcwd(), "requirements.txt")
            if os.path.exists(req_path):
                print("Installing requirements.txt...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path], check=True)
            else:
                subprocess.run([sys.executable, "-m", "pip", "install", "numpy", "pandas", "torch", "redis", "pydantic", "pokerkit", "python-dotenv", "requests", "jsonschema", "flask", "urllib3"], check=True)
            print("Dependencies successfully installed!")
        except Exception as e:
            print(f"Failed to auto-install dependencies: {e}.")
            
        still_missing = []
        for pkg in required_packages:
            try:
                if pkg == "dotenv":
                    import dotenv
                else:
                    with silence_kaggle_warnings():
                        __import__(pkg)
            except ImportError:
                still_missing.append(pkg)
                
        if still_missing:
            print("\n" + "="*80)
            print(f"CRITICAL ERROR: The following packages are still missing: {still_missing}")
            print("Please run manually on this machine:")
            print("  pip install " + " ".join(still_missing))
            print("="*80 + "\n")
            print("Worker will pause for 60 seconds before exiting to prevent infinite crash loops...")
            time.sleep(60)
            sys.exit(1)
