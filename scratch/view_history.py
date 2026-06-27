import json
from pathlib import Path

def main():
    p = Path("versions/version_history.json")
    if not p.exists():
        print("No version history file found.")
        return
        
    data = json.loads(p.read_text(encoding="utf-8"))
    
    # Print keys of the last entry
    if data:
        print("Keys in the last entry:")
        print(list(data[-1].keys()))
        print("\nLast entry details:")
        # print first 500 chars of entry representation
        print(str(data[-1])[:1000])

if __name__ == "__main__":
    main()
