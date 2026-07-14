import json
import sys
from pathlib import Path
from collections import Counter

# Add project root to sys.path
cwd = str(Path(__file__).parent.parent.resolve())
if cwd not in sys.path:
    sys.path.insert(0, cwd)

from cb_agents.card_registry import CardRegistry

def main():
    replay_path = Path("logs/kaggle_replays/episode-85904195-replay.json")
    if not replay_path.exists():
        print("Replay episode-85904195-replay.json not found")
        return
        
    data = json.loads(replay_path.read_text(encoding="utf-8"))
    steps = data.get("steps", [])
    print(f"Total steps: {len(steps)}")
    
    player_idx = 0 # We are Player 0
    opp_idx = 1
    
    reg = CardRegistry(skills_dir="skills")
    
    def get_card_name(cid):
        if cid is None:
            return "None"
        card = reg.get(int(cid))
        return card.card_name if card else f"Card {cid}"

    # Trace the last 30 steps of the game
    start_step = max(0, len(steps) - 40)
    print(f"Tracing game from Step {start_step} to {len(steps)-1}...")
    
    for idx in range(start_step, len(steps)):
        step = steps[idx]
        if len(step) <= player_idx:
            continue
            
        p_state = step[player_idx]
        opp_state = step[opp_idx]
        
        action = p_state.get("action")
        status = p_state.get("status")
        reward = p_state.get("reward")
        
        obs = p_state.get("observation", {}) or {}
        select = obs.get("select")
        current = obs.get("current") or {}
        players = current.get("players", [])
        
        if len(players) > player_idx:
            our_player = players[player_idx]
            opp_player = players[opp_idx]
            
            active = our_player.get("active", [])
            bench = our_player.get("bench", [])
            hand = our_player.get("hand", []) or []
            deck = our_player.get("deck", []) or []
            prizes = len(our_player.get("prize", []))
            
            opp_active = opp_player.get("active", [])
            opp_bench = opp_player.get("bench", [])
            opp_deck = opp_player.get("deck", []) or []
            opp_prizes = len(opp_player.get("prize", []))
            
            active_desc = "None"
            if active:
                a_card = active[0] if isinstance(active, list) else active
                if isinstance(a_card, dict):
                    att = a_card.get("attached", []) or a_card.get("energies", []) or []
                    att_desc = [get_card_name(e.get("id") if isinstance(e, dict) else e) for e in att]
                    active_desc = f"{get_card_name(a_card.get('id'))} (HP: {a_card.get('hp')}/{a_card.get('maxHp')}, Energies: {att_desc})"
                    
            opp_active_desc = "None"
            if opp_active:
                oa_card = opp_active[0] if isinstance(opp_active, list) else opp_active
                if isinstance(oa_card, dict):
                    oatt = oa_card.get("attached", []) or oa_card.get("energies", []) or []
                    oatt_desc = [get_card_name(e.get("id") if isinstance(e, dict) else e) for e in oatt]
                    opp_active_desc = f"{get_card_name(oa_card.get('id'))} (HP: {oa_card.get('hp')}/{oa_card.get('maxHp')}, Energies: {oatt_desc})"
            
            bench_names = [get_card_name(b.get('id')) for b in bench if isinstance(b, dict)]
            hand_names = [get_card_name(h_card.get('id') if isinstance(h_card, dict) else h_card) for h_card in hand]
            
            print(f"\n[Step {idx}] Status={status} Reward={reward}")
            print(f"  Us : Active={active_desc} | Bench={bench_names} | Hand={len(hand)} | Deck={len(deck)} | Prizes={prizes}")
            print(f"  Opp: Active={opp_active_desc} | Bench={len(opp_bench)} | Deck={len(opp_deck)} | Prizes={opp_prizes}")
            
            if select:
                sel_ctx = select.get("context")
                sel_type = select.get("type")
                options = select.get("option", [])
                
                print(f"  Select: type={sel_type}, context={sel_ctx}, options_count={len(options)}")
                if action:
                    selected_opts = []
                    for o in action:
                        if o < len(options):
                            opt = options[o]
                            opt_type = opt.get("type")
                            opt_name = get_card_name(opt.get("id")) if opt.get("id") else opt.get("name", "unnamed")
                            selected_opts.append(f"{opt_name} (type {opt_type})")
                    print(f"  -> Chosen indices: {action} ({selected_opts})")

if __name__ == "__main__":
    main()
