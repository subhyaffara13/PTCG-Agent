import sys
import os
from pathlib import Path

# Ensure correct path resolution
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

from scratch.deck_optimizer import main

if __name__ == '__main__':
    print("--- Running GA Deck Optimizer debug run ---")
    try:
        main()
        print("GA main completed successfully.")
    except Exception as e:
        import traceback
        print("GA main crashed with exception:")
        traceback.print_exc()

    path = "agents/deck_new.csv"
    print(f"Checking '{path}':")
    print("  Exists:", os.path.exists(path))
    if os.path.exists(path):
        print("  Size:", os.path.getsize(path))
        print("  First 5 lines:")
        with open(path, "r", encoding="utf-8") as f:
            for _ in range(5):
                line = f.readline()
                if not line: break
                print("    ", line.strip())
