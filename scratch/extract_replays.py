"""
scratch/extract_replays.py
Extracts winning and losing decks from Kaggle replays, categorizing by team.
"""
import os
import json
from pathlib import Path
from collections import Counter

def is_us(name: str) -> bool:
    return "subhy" in name.lower() or "antigravity" in name.lower()

def main():
    replay_dir = Path("logs/kaggle_replays")
    out_dir = Path("logs/kaggle_summary")
    out_dir.mkdir(parents=True, exist_ok=True)

    opp_wins, us_wins, us_losses = Counter(), Counter(), Counter()
    opp_win_decks, us_win_decks, us_loss_decks = [], [], []

    print("Extracting detailed decks from replays...")
    for f in replay_dir.glob("*.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            steps, rewards = d.get("steps", []), d.get("rewards", [0, 0])
            info = d.get("info", {})
            teams = info.get("TeamNames", ["Unknown", "Unknown"])
            if len(steps) < 2 or len(rewards) < 2 or len(teams) < 2:
                continue

            decks = [steps[1][0].get("action"), steps[1][1].get("action")]
            if not all(isinstance(dk, list) and len(dk) == 60 for dk in decks):
                continue

            for idx in [0, 1]:
                name, deck, reward = teams[idx], decks[idx], rewards[idx]
                other_reward = rewards[1 - idx]
                
                if is_us(name):
                    if reward > other_reward:
                        us_wins.update(deck)
                        us_win_decks.append(deck)
                    else:
                        us_losses.update(deck)
                        us_loss_decks.append(deck)
                else:
                    if reward > other_reward:
                        opp_wins.update(deck)
                        opp_win_decks.append(deck)
        except Exception as e:
            pass

    summary = {
        "opp_wins": dict(opp_wins),
        "us_wins": dict(us_wins),
        "us_losses": dict(us_losses),
        "opp_win_decks": opp_win_decks,
        "us_win_decks": us_win_decks,
        "us_loss_decks": us_loss_decks
    }
    out_file = out_dir / "scraped_decks.json"
    out_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Scraped Opponent Wins: {len(opp_win_decks)}, Our Wins: {len(us_win_decks)}, Our Losses: {len(us_loss_decks)}")

if __name__ == "__main__":
    main()
