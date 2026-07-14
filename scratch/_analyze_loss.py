import json, sys
from pathlib import Path

sys.path.insert(0, "C:/Users/subhy/.gemini/antigravity/scratch/ptcg-agent")

replays_dir = Path("C:/Users/subhy/.gemini/antigravity/scratch/ptcg-agent/logs/kaggle_replays")
replay_files = sorted(replays_dir.glob("episode-*-replay.json"), key=lambda p: p.stat().st_mtime, reverse=True)

for replay_file in replay_files[:5]:
    print(f"\n{'='*60}")
    print(f"Analyzing: {replay_file.name}")
    print(f"{'='*60}")
    
    data = json.loads(replay_file.read_text(encoding="utf-8"))
    steps = data.get("steps", [])
    info = data.get("info", {})
    team_names = info.get("TeamNames", ["Unknown", "Unknown"])
    agents = info.get("Agents", [])
    
    my_idx = -1
    for idx, name in enumerate(team_names):
        if "Subhy" in name:
            my_idx = idx
            break
    if my_idx == -1:
        my_idx = 1  # fallback
    
    opp_idx = 1 - my_idx
    print(f"Teams: {team_names[0]} vs {team_names[1]}")
    print(f"We are Player {my_idx}")
    
    last_step = steps[-1]
    my_final = last_step[my_idx] if my_idx < len(last_step) else {}
    opp_final = last_step[opp_idx] if opp_idx < len(last_step) else {}
    
    my_obs = my_final.get("observation", {}) or {}
    my_curr = my_obs.get("current", {}) or {}
    players = my_curr.get("players", [])
    
    if len(players) > my_idx:
        mp = players[my_idx]
        op = players[opp_idx] if len(players) > opp_idx else {}
        print(f"\nFinal state:")
        print(f"  Us: status={my_final.get('status')}, reward={my_final.get('reward')}")
        print(f"  Our deckCount={mp.get('deckCount')}, hand={len(mp.get('hand',[]) or [])}, bench={len(mp.get('bench',[]) or [])}, prize={len(mp.get('prize',[]) or [])}")
        print(f"  Opp: status={opp_final.get('status')}, reward={opp_final.get('reward')}")
        if op:
            print(f"  Opp deckCount={op.get('deckCount')}, hand={len(op.get('hand',[]) or [])}, bench={len(op.get('bench',[]) or [])}, prize={len(op.get('prize',[]) or [])}")
    
    logs = my_obs.get("logs", [])
    print(f"\nLast 5 logs:")
    for log in logs[-5:]:
        print(f"  {log}")
    
    # Track deck count over time
    print(f"\nDeck count progression (when it changes):")
    prev_dc = None
    for i, step in enumerate(steps):
        if my_idx < len(step):
            p_state = step[my_idx]
            obs = p_state.get("observation", {}) or {}
            curr = obs.get("current", {}) or {}
            pls = curr.get("players", [])
            if len(pls) > my_idx and pls[my_idx] is not None:
                dc = pls[my_idx].get("deckCount")
                if dc is not None and dc != prev_dc:
                    print(f"  Step {i}: deckCount={dc}, hand={len(pls[my_idx].get('hand',[]) or [])}")
                    prev_dc = dc
    
    # Check when deck went to 0 or below
    print(f"\nSearching for deck_out events...")
    for i, step in enumerate(steps):
        if my_idx < len(step):
            p_state = step[my_idx]
            obs = p_state.get("observation", {}) or {}
            curr = obs.get("current", {}) or {}
            pls = curr.get("players", [])
            if len(pls) > my_idx and pls[my_idx] is not None:
                dc = pls[my_idx].get("deckCount")
                if dc is not None and dc <= 1:
                    action = p_state.get("action", [])
                    select = obs.get("select", {})
                    ctx = select.get("context") if select else None
                    st = select.get("type") if select else None
                    opts = select.get("option", []) if select else []
                    opts_info = [(o.get("type"), o.get("name","")) for o in opts[:5]]
                    print(f"  Step {i}: deckCount={dc}, action={action}, select_ctx={ctx}, select_type={st}, options_preview={opts_info}")
                    if dc == 0:
                        # Check previous steps for what caused it
                        for j in range(max(0,i-3), i):
                            prev_step = steps[j]
                            if my_idx < len(prev_step):
                                pp = prev_step[my_idx]
                                po = pp.get("observation",{}) or {}
                                pc = po.get("current",{}) or {}
                                ppl = pc.get("players",[])
                                if len(ppl) > my_idx and ppl[my_idx] is not None:
                                    pdc = ppl[my_idx].get("deckCount")
                                    pa = pp.get("action",[])
                                    print(f"    Step {j} (before 0): deckCount={pdc}, action={pa}")

print("\nDone.")
