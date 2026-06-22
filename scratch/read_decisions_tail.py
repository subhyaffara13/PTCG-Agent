import sys
from pathlib import Path

def main():
    decisions_path = Path("decisions.md")
    if not decisions_path.exists():
        print("decisions.md not found.")
        return
    
    lines = decisions_path.read_text(encoding="utf-8").splitlines()
    print(f"Total lines: {len(lines)}")
    print("\n--- LAST 100 LINES ---\n")
    for line in lines[-100:]:
        print(line)

if __name__ == "__main__":
    main()
