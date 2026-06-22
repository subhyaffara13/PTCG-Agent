import json
from pathlib import Path

def main():
    replay_file = Path("logs/kaggle_replays/episode-81180473-replay.json")
    data = json.loads(replay_file.read_text(encoding="utf-8"))
    steps = data.get("steps", [])
    
    # Print the details of step 0, player 0 and step 1, player 0
    print("Step 10 Player 0 Observation keys:")
    obs_10 = steps[10][0].get("observation", {}) or {}
    print(list(obs_10.keys()))
    print("Step 10 Player 0 Observation 'current' type/content:")
    curr = obs_10.get("current")
    if curr:
        print(type(curr))
        if isinstance(curr, dict):
            print(list(curr.keys()))
        else:
            print(str(curr)[:200])
    
    print("Step 10 Player 0 Action:")
    print(steps[10][0].get("action"))
    
    # Check what players are in data['info'] or other places
    print(f"Info keys: {list(data.get('info', {}).keys())}")
    print(f"Info content: {data.get('info')}")

if __name__ == "__main__":
    main()
