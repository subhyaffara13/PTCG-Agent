"""
scratch/extract_failed.py
Parses version_history.json to analyze baseline check failures.
"""
import json
from pathlib import Path

def main():
    history_file = Path("versions/version_history.json")
    out_dir = Path("logs/kaggle_summary")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    failed_versions = []
    
    if history_file.exists():
        try:
            history = json.loads(history_file.read_text(encoding="utf-8"))
            for entry in history:
                if not entry.get("promoted") and entry.get("failed_check") == 8:
                    failed_versions.append({
                        "version_id": entry.get("version_id"),
                        "reason": entry.get("reason"),
                        "timestamp": entry.get("timestamp")
                    })
        except Exception as e:
            print(f"Error loading version history: {e}")
            
    out_file = out_dir / "failed_decks.json"
    out_file.write_text(json.dumps(failed_versions, indent=2), encoding="utf-8")
    print(f"Logged {len(failed_versions)} failed baseline versions to {out_file}")

if __name__ == "__main__":
    main()
