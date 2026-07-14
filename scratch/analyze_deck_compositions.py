import os
import sys
import json
from pathlib import Path
from collections import Counter

# Add project root to sys.path
cwd = str(Path(__file__).parent.parent.resolve())
if cwd not in sys.path:
    sys.path.insert(0, cwd)

from factory.deck_loader import DeckLoader

def main():
    loader = DeckLoader(Path("skills"))
    pool = loader.load_card_pool()
    card_names = {int(c["card_id"]): c.get("card_name", f"Card {c['card_id']}") for c in pool if str(c.get("card_id", "")).isdigit()}

    replays_dir = Path("logs/kaggle_replays")
    replay_files = sorted(replays_dir.glob("episode-*-replay.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    
    for path in replay_files[:5]:
        print(f"\n==================================================")
        print(f"EPISODE: {path.stem}")
        print(f"==================================================")
        
        try:
            data = json.load(path.open("r", encoding="utf-8"))
        except Exception as e:
            print(f"Failed to load: {e}")
            continue

        steps = data.get("steps", [])
        if len(steps) < 2:
            continue
            
        info = data.get("info", {})
        team_names = info.get("TeamNames", ["Player 0", "Player 1"])
        
        # We can find all card IDs introduced in Step 1 for both players
        # Step 1 action is the initial deck list of cards (often the whole list of integers)
        step1 = steps[1]
        
        for p_idx, player in enumerate(step1):
            action = player.get("action", [])
            # Action at step 1 contains the deck list of 60 card IDs
            deck_card_ids = [int(cid) for cid in action if str(cid).isdigit()]
            if len(deck_card_ids) == 60:
                card_counts = Counter(card_names.get(cid, f"Card {cid}") for cid in deck_card_ids)
                print(f"\nPlayer {p_idx} ({team_names[p_idx]}) Deck List:")
                for name, count in sorted(card_counts.items(), key=lambda x: x[0]):
                    print(f"  - {count}x {name}")
            else:
                print(f"\nPlayer {p_idx} ({team_names[p_idx]}) - Initial action length {len(action)} (not 60)")

if __name__ == "__main__":
    main()
