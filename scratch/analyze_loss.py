import json
from pathlib import Path

def main():
    replay_file = Path("logs/kaggle_replays/episode-84349575-replay.json")
    if not replay_file.exists():
        print("Replay file not found.")
        return
        
    data = json.loads(replay_file.read_text(encoding="utf-8"))
    steps = data.get("steps", [])
    print(f"Total steps: {len(steps)}")
    
    # Let's inspect step 1 to see the decks submitted
    if len(steps) > 1:
        # Player 0 deck
        p0_deck = steps[1][0].get("action", [])
        p1_deck = steps[1][1].get("action", [])
        print(f"Player 0 Deck Size: {len(p0_deck)}")
        print(f"Player 1 Deck Size: {len(p1_deck)}")
        print(f"Player 0 Deck First 10: {p0_deck[:10]}")
        print(f"Player 1 Deck First 10: {p1_deck[:10]}")
        
    # Let's trace steps and print actions taken by each player
    for idx, step in enumerate(steps):
        if idx < 2:
            continue
            
        p0 = step[0]
        p1 = step[1]
        
        p0_action = p0.get("action", [])
        p1_action = p1.get("action", [])
        p0_status = p0.get("status")
        p1_status = p1.get("status")
        
        # Check active player (who took an action)
        if p0_action and p0_action != [0]:
            print(f"Step {idx:03d} (Player 0 Active): status={p0_status}, action={p0_action}")
        if p1_action and p1_action != [0]:
            print(f"Step {idx:03d} (Player 1 Active): status={p1_status}, action={p1_action}")
            
    # Print final rewards
    last_step = steps[-1]
    print(f"\nFinal Rewards:")
    print(f"  Player 0: {last_step[0].get('reward')} (status={last_step[0].get('status')})")
    print(f"  Player 1: {last_step[1].get('reward')} (status={last_step[1].get('status')})")

if __name__ == "__main__":
    main()
