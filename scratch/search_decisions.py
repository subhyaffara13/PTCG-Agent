import os
from pathlib import Path

def main():
    p = Path("decisions.md")
    if not p.exists():
        print("decisions.md not found.")
        return
    content = p.read_text(encoding="utf-8")
    print(content[-4000:])

if __name__ == "__main__":
    main()
