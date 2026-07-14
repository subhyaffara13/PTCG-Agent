import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, "C:/Users/subhy/.gemini/antigravity/scratch/ptcg-agent")

from cb_agents.card_registry import CardRegistry

def main():
    replay_path = Path("logs/kaggle_replays/episode-85445580-replay.json")
    if not replay_path.exists():
        print("Replay not found")
        return
        
    data = json.loads(replay_path.read_text(encoding="utf-8"))
    steps = data.get("steps", [])
    print(f"Total steps: {len(steps)}")
    
    player_idx = 0 # We were Player 0 in this game
    opp_idx = 1
    
    reg = CardRegistry(skills_dir="skills")
    
    def get_card_name(cid):
        if cid is None:
            return "None"
        card = reg.get(int(cid))
        return card.card_name if card else f"Unknown({cid})"
        
    # Trace through the game steps to see our board state and actions
    for idx, step in enumerate(steps):
        if len(step) <= player_idx:
            continue
        p_state = step[player_idx]
        action = p_state.get("action")
        obs = p_state.get("observation", {}) or {}
        select = obs.get("select")
        current = obs.get("current") or {}
        players = current.get("players", [])
        
        # Print when we chose an action or when our hand/active changed
        if len(players) > player_idx:
            our_player = players[player_idx]
            opp_player = players[opp_idx]
            
            active = our_player.get("active", [])
            bench = our_player.get("bench", [])
            hand = our_player.get("hand", []) or []
            hand_count = our_player.get("handCount", 0)
            prizes = len(our_player.get("prize", []))
            
            opp_active = opp_player.get("active", [])
            opp_bench = opp_player.get("bench", [])
            opp_prizes = len(opp_player.get("prize", []))
            
            if idx % 5 == 0 or (select and action):
                sel_ctx = select.get("context") if select else None
                sel_type = select.get("type") if select else None
                
                active_desc = "None"
                if active and isinstance(active[0], dict):
                    active_desc = f"{get_card_name(active[0].get('id'))} (HP: {active[0].get('hp')}/{active[0].get('maxHp')}, Energies: {active[0].get('energies')})"
                    
                opp_active_desc = "None"
                if opp_active and isinstance(opp_active[0], dict):
                    opp_active_desc = f"{get_card_name(opp_active[0].get('id'))} (HP: {opp_active[0].get('hp')}/{opp_active[0].get('maxHp')}, Energies: {opp_active[0].get('energies')})"
                
                bench_names = [get_card_name(b.get('id')) for b in bench if isinstance(b, dict)]
                hand_names = [get_card_name(h_card.get('id') if isinstance(h_card, dict) else h_card) for h_card in hand]
                
                print(f"Step {idx:3d}: Us Active={active_desc} | Bench={bench_names} | Hand={hand_names} | Prizes={prizes}")
                print(f"         Opp Active={opp_active_desc} | Bench={len(opp_bench)} | Prizes={opp_prizes}")
                if select and action:
                    options = select.get("option", [])
                    selected_opts = []
                    for o in action:
                        if o < len(options):
                            opt = options[o]
                            opt_type = opt.get("type")
                            opt_name = get_card_name(opt.get("id")) if opt.get("id") else opt.get("name", "unnamed")
                            selected_opts.append(f"{opt_name} (type {opt_type})")
                    print(f"       -> Action context={sel_ctx}, Chosen={selected_opts}")

if __name__ == "__main__":
    main()
