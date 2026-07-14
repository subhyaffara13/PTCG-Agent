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

def load_card_names():
    try:
        loader = DeckLoader(Path("skills"))
        pool = loader.load_card_pool()
        return {int(c["card_id"]): c.get("card_name", f"Card {c['card_id']}") for c in pool if str(c.get("card_id", "")).isdigit()}
    except Exception as e:
        print(f"Warning: could not load card names: {e}")
        return {}

def analyze_losses():
    card_names = load_card_names()
    replays_dir = Path("logs/kaggle_replays")
    if not replays_dir.exists():
        print("No kaggle replays found.")
        return

    # Find the most recently modified replays
    replay_files = sorted(replays_dir.glob("episode-*-replay.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not replay_files:
        print("No replay JSON files found.")
        return

    print(f"Analyzing the latest {min(5, len(replay_files))} replays out of {len(replay_files)} total:")
    for path in replay_files[:5]:
        print(f"\n==================================================")
        print(f"EPISODE: {path.stem}")
        print(f"==================================================")
        
        try:
            data = json.load(path.open("r", encoding="utf-8"))
        except Exception as e:
            print(f"Failed to load replay: {e}")
            continue

        steps = data.get("steps", [])
        if not steps:
            print("Empty replay.")
            continue

        info = data.get("info", {})
        team_names = info.get("TeamNames", ["Player 0", "Player 1"])
        agents = info.get("Agents", [])
        
        # Determine player index
        my_idx = -1
        opp_name = "Opponent"
        for idx, agent in enumerate(agents):
            name = agent.get("Name", "")
            if "Subhy" in name or "subhy" in name:
                my_idx = idx
            else:
                opp_name = name

        if my_idx == -1:
            for idx, name in enumerate(team_names):
                if "Subhy" in name or "subhy" in name:
                    my_idx = idx
                else:
                    opp_name = name

        if my_idx == -1:
            print("Could not identify our player index. Defaulting to Player 0.")
            my_idx = 0
            opp_name = team_names[1]

        opp_idx = 1 - my_idx
        print(f"We are Player {my_idx} ({team_names[my_idx]})")
        print(f"Opponent is Player {opp_idx} ({opp_name})")

        # Check final step rewards
        final_step = steps[-1]
        my_final = final_step[my_idx] if my_idx < len(final_step) else {}
        opp_final = final_step[opp_idx] if opp_idx < len(final_step) else {}
        
        my_reward = my_final.get("reward", 0)
        opp_reward = opp_final.get("reward", 0)
        my_status = my_final.get("status")
        opp_status = opp_final.get("status")

        print(f"Outcome: Reward={my_reward} (Status={my_status}) | Opponent Reward={opp_reward} (Status={opp_status})")
        if my_reward is not None and opp_reward is not None:
            if my_reward > opp_reward:
                print("Result: WIN")
            elif my_reward < opp_reward:
                print("Result: LOSS")
            else:
                print("Result: DRAW")

        # Stderr logs check
        my_stderr = my_final.get("stderr", "")
        opp_stderr = opp_final.get("stderr", "")
        if my_stderr:
            print(f"Our Stderr:\n{my_stderr.strip()}")
        if opp_stderr:
            print(f"Opponent Stderr:\n{opp_stderr.strip()}")

        # Look at observation logs or game states
        obs = my_final.get("observation", {}) or {}
        curr = obs.get("current", {}) or {}
        players = curr.get("players", [])
        
        if len(players) > 1:
            my_state = players[my_idx]
            opp_state = players[opp_idx]
            
            my_hand = my_state.get("hand") or []
            opp_hand = opp_state.get("hand") or []
            my_prizes = len(my_state.get("prize") or [])
            opp_prizes = len(opp_state.get("prize") or [])
            my_deck_size = len(my_state.get("deck") or [])
            opp_deck_size = len(opp_state.get("deck") or [])
            
            print(f"Prizes remaining: Us {my_prizes} | Opponent {opp_prizes}")
            print(f"Deck cards remaining: Us {my_deck_size} | Opponent {opp_deck_size}")
            
            # Print active Pokemon
            my_active = my_state.get("active")
            opp_active = opp_state.get("active")
            
            def get_card_desc(card):
                if not card:
                    return "None"
                if isinstance(card, list):
                    if not card: return "None"
                    card = card[0]
                cid = card.get("card_id") if isinstance(card, dict) else card
                if isinstance(cid, list):
                    if not cid: cid = None
                    else: cid = cid[0]
                try:
                    name = card_names.get(int(cid), f"Card {cid}") if cid is not None else "Unknown"
                except Exception:
                    name = f"Card {cid}"
                hp = card.get("hp") if isinstance(card, dict) else None
                return f"{name} (HP: {hp})" if hp else name

            print(f"Active Pokemon: Us [{get_card_desc(my_active)}] | Opponent [{get_card_desc(opp_active)}]")
            
            # Show our hand content summary
            print(f"Hand size: Us {len(my_hand)} | Opponent {len(opp_hand)}")
            
            my_hand_names = [card_names.get(int(c), f"Card {c}") for c in my_hand if str(c).isdigit()]
            print(f"Our Hand: {Counter(my_hand_names)}")
            
            # Show bench sizes
            print(f"Bench size: Us {len(my_state.get('bench') or [])} | Opponent {len(opp_state.get('bench') or [])}")
            
        # Check last 5 game logs for why the game ended
        logs = obs.get("logs", [])
        if logs:
            print("Last 10 game logs:")
            for log in logs[-10:]:
                print(f"  - {log}")

if __name__ == "__main__":
    analyze_losses()
