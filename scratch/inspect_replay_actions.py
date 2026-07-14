import json
from pathlib import Path

def main():
    replay_path = Path("logs/kaggle_replays/episode-80470780-replay.json")
    if not replay_path.exists():
        print("Replay not found")
        return
        
    data = json.loads(replay_path.read_text(encoding="utf-8"))
    steps = data.get("steps", [])
    
    player_idx = 0
    printed_types = set()
    for idx, step in enumerate(steps):
        if len(step) <= player_idx:
            continue
        p_state = step[player_idx]
        action = p_state.get("action")
        obs = p_state.get("observation", {}) or {}
        select = obs.get("select")
        
        if select and action:
            sel_type = select.get("type")
            sel_ctx = select.get("context")
            key = (sel_type, sel_ctx)
            if key not in printed_types:
                printed_types.add(key)
                options = select.get("option", [])
                print(f"\n--- UNIQUE SELECT: type={sel_type}, context={sel_ctx} ---")
                print("First 10 options:")
                for o_idx, opt in enumerate(options[:10]):
                    print(f"  [{o_idx}]: {opt}")
                print("Action chosen:", action)

if __name__ == "__main__":
    main()
