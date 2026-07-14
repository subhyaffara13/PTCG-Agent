import json
from pathlib import Path

def main():
    replay_path = Path("logs/kaggle_replays/episode-85904195-replay.json")
    if not replay_path.exists():
        print("Replay not found")
        return
        
    data = json.load(replay_path.open("r", encoding="utf-8"))
    steps = data.get("steps", [])
    
    # We are Player 0
    p_idx = 0
    
    # Let's inspect step 51 (when our deck size hit 0)
    step = steps[51]
    p_state = step[p_idx]
    obs = p_state.get("observation", {}) or {}
    curr = obs.get("current", {}) or {}
    players = curr.get("players", [])
    
    if len(players) > p_idx:
        p0 = players[p_idx]
        print("=== PLAYER 0 STATE AT STEP 51 ===")
        print(f"Hand: {p0.get('hand')}")
        print(f"Deck Size: {len(p0.get('deck', []))}")
        print(f"Discard Pile: {p0.get('discard')}")
        print(f"Prizes: {p0.get('prize')}")
        
        # Check active and bench
        active = p0.get("active", [])
        print(f"Active: {active}")
        bench = p0.get("bench", [])
        for i, b in enumerate(bench):
            print(f"Bench {i}: {b}")
            
if __name__ == "__main__":
    main()
