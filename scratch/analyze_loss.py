import json
from pathlib import Path

def main():
    # Load a loss replay: episode 81179844 vs persist
    replay_file = Path("logs/kaggle_replays/episode-81179844-replay.json")
    if not replay_file.exists():
        print("Replay file not found!")
        return
        
    data = json.loads(replay_file.read_text(encoding="utf-8"))
    steps = data.get("steps", [])
    print(f"Total steps: {len(steps)}")
    
    # Let's check who the players are
    info = data.get("info", {})
    print(f"Players: {info.get('TeamNames')}")
    
    # We want to identify the action history of both players, especially in the last 20 steps
    print("\n--- Last 10 steps actions and rewards ---")
    for i in range(max(0, len(steps)-10), len(steps)):
        step = steps[i]
        print(f"Step {i}:")
        for p_idx, player_state in enumerate(step):
            act = player_state.get("action")
            reward = player_state.get("reward")
            status = player_state.get("status")
            print(f"  Player {p_idx}: action={act}, reward={reward}, status={status}")
            
    # Let's inspect step 20, 40, 60 to see typical moves
    print("\n--- Mid-game check (Steps 20, 50, 80) ---")
    for step_num in [20, 50, 80]:
        if step_num < len(steps):
            step = steps[step_num]
            print(f"Step {step_num}:")
            for p_idx, player_state in enumerate(step):
                act = player_state.get("action")
                print(f"  Player {p_idx}: action={act}")

if __name__ == "__main__":
    main()
