import json
from pathlib import Path

def main():
    replay_path = Path("logs/kaggle_replays/episode-85904195-replay.json")
    if not replay_path.exists():
        print("Replay not found")
        return
        
    data = json.load(replay_path.open("r", encoding="utf-8"))
    steps = data.get("steps", [])
    
    for idx in range(min(5, len(steps))):
        step = steps[idx]
        print(f"\n=== STEP {idx} ===")
        for p_idx, player in enumerate(step):
            stderr = player.get("stderr", "")
            if stderr:
                print(f"  Player {p_idx} Stderr:\n{stderr.strip()}")
            else:
                print(f"  Player {p_idx} Stderr: Empty")

if __name__ == "__main__":
    main()
