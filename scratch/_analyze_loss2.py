import json, sys
from pathlib import Path

replay_file = Path("C:/Users/subhy/.gemini/antigravity/scratch/ptcg-agent/logs/kaggle_replays/episode-85639932-replay.json")
data = json.loads(replay_file.read_text(encoding="utf-8"))
steps = data.get("steps", [])
info = data.get("info", {})
team_names = info.get("TeamNames", ["Unknown", "Unknown"])
my_idx = 0

print("Detailed step-by-step analysis:")
for i in range(len(steps)):
    step = steps[i]
    if my_idx >= len(step):
        continue
    ps = step[my_idx]
    obs = ps.get("observation", {}) or {}
    curr = obs.get("current", {}) or {}
    select = obs.get("select", {}) or {}
    sel_type = select.get("type")
    sel_ctx = select.get("context")
    action = ps.get("action", [])
    players = curr.get("players", [])
    
    mp = players[my_idx] if len(players) > my_idx and players[my_idx] else {}
    dc = mp.get("deckCount")
    hand = len(mp.get("hand", []) or [])
    bench = len(mp.get("bench", []) or [])
    prizes = len(mp.get("prize", []) or [])
    
    opts = select.get("option", []) or []
    n_opts = len(opts)
    sel_type_name = {0:"main",1:"choice",2:"prize",4:"discard",7:"energy",9:"starter"}.get(sel_type, str(sel_type))
    
    selected_info = ""
    if action and n_opts > 0:
        aidx = action[0]
        if aidx < n_opts:
            opt = opts[aidx]
            selected_info = f"type={opt.get('type')} name={opt.get('name','')}"
        else:
            selected_info = f"OUT_OF_RANGE({aidx})"
    
    # Only print if it's our turn with main select or any action
    if sel_type == 0 or action:
        print(f"Step {i:3d}: sel={sel_type_name}({sel_ctx}) act={str(action):10s} dc={dc} hand={hand} bench={bench} prizes={prizes} n_opts={n_opts} {selected_info}")
