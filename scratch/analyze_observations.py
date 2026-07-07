import json
from pathlib import Path

def main():
    replay_file = Path("logs/kaggle_replays/episode-84349575-replay.json")
    if not replay_file.exists():
        print("Replay file not found.")
        return
        
    data = json.loads(replay_file.read_text(encoding="utf-8"))
    steps = data.get("steps", [])
    
    # We want to print states for Player 0 active turns
    for idx, step in enumerate(steps):
        if idx < 2:
            continue
            
        p0 = step[0]
        p0_action = p0.get("action", [])
        
        # If Player 0 took a non-trivial action or choice
        if p0_action and p0_action != [0]:
            print(f"\n==================================================")
            print(f"STEP {idx} (Player 0 Active): action={p0_action}")
            print(f"==================================================")
            
            obs = p0.get("observation", {}) or {}
            
            # Print select choice prompt
            select = obs.get("select")
            if select:
                print(f"Select prompt type: {select.get('type')}")
                print(f"Select prompt options: {select.get('option')}")
                print(f"Select prompt maxCount: {select.get('maxCount')}")
                
            # Print simple board state details if available
            # Observation keys:
            # Let's print the general keys to see what is inside
            keys_to_print = ['my_deck_count', 'opponent_deck_count', 'my_hand_count', 'opponent_hand_count', 
                             'my_prize_count', 'opponent_prize_count', 'my_active', 'opponent_active']
            for k in keys_to_print:
                if k in obs:
                    print(f"  {k}: {obs[k]}")

if __name__ == "__main__":
    main()
