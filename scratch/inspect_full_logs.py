import json
from pathlib import Path

def main():
    replay_path = Path("logs/kaggle_replays/episode-85904195-replay.json")
    if not replay_path.exists():
        print("Replay not found")
        return
        
    data = json.load(replay_path.open("r", encoding="utf-8"))
    steps = data.get("steps", [])
    
    # We want to print all log events from all steps to see the narrative of the game
    print("=== FULL GAME LOG EVENTS ===")
    for idx, step in enumerate(steps):
        # Step is a list of player states. We can check either player's observation logs
        # as they contain the public log events of the turn.
        logs = []
        for p_state in step:
            obs = p_state.get("observation", {}) or {}
            step_logs = obs.get("logs", [])
            if step_logs:
                logs = step_logs
                break
        
        if logs:
            print(f"\nStep {idx}:")
            for log in logs:
                print(f"  {log}")

if __name__ == "__main__":
    main()
