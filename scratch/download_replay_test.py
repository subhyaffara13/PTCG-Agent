import json
import subprocess
from pathlib import Path

def main():
    episode_id = 81180473
    output_dir = Path("logs/kaggle_replays")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = ["kaggle", "competitions", "replay", str(episode_id), "-p", str(output_dir)]
    print(f"Running command: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print("Download completed.")
    
    replay_file = output_dir / f"episode-{episode_id}-replay.json"
    if replay_file.exists():
        data = json.loads(replay_file.read_text(encoding="utf-8"))
        print(f"Keys in replay: {list(data.keys())}")
        
        # Let's inspect the first step and the last step
        steps = data.get("steps", [])
        print(f"Number of steps: {len(steps)}")
        if steps:
            print("First step rewards/status:")
            for idx, p in enumerate(steps[0]):
                print(f"  Player {idx}: reward={p.get('reward')}, status={p.get('status')}")
            print("Last step rewards/status:")
            for idx, p in enumerate(steps[-1]):
                print(f"  Player {idx}: reward={p.get('reward')}, status={p.get('status')}")
            
            # Print the observation keys
            obs = steps[0][0].get("observation", {}) or {}
            print(f"Observation keys in step 0, player 0: {list(obs.keys())}")
            
            # Let's see if we can find my_deck or opponent_deck
            print(f"my_deck_count: {obs.get('my_deck_count')}")
            
if __name__ == "__main__":
    main()
