"""Debug test: Trace exactly what the CABT environment sends and what we return."""
import sys
import os
from pathlib import Path

script_dir = Path(__file__).parent.resolve()
workspace_dir = script_dir.parent
sys.path.insert(0, str(workspace_dir / "submission"))
os.chdir(str(workspace_dir / "submission"))

from kaggle_environments import make

call_count = 0

def debug_agent(obs, config):
    global call_count
    call_count += 1
    
    if obs.select is None:
        DEFAULT_DECK = [
            721, 721, 722, 722, 722, 722, 723, 723, 723, 723,
            1092, 1121, 1121, 1145, 1145, 1163, 1163, 1219,
            1219, 1219, 1219, 1227, 1227, 1227, 1227, 1262,
            1262, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3
        ]
        print(f"Call {call_count}: Deck submission (select=None)")
        return DEFAULT_DECK
    
    options = getattr(obs.select, "option", [])
    max_count = getattr(obs.select, "maxCount", 1)
    sel_type = getattr(obs.select, "type", None)
    sel_ctx = getattr(obs.select, "context", None)
    
    fallback = list(range(min(max_count, len(options))))
    
    if not fallback:
        print(f"Call {call_count}: EMPTY FALLBACK! type={sel_type}, ctx={sel_ctx}, options={len(options)}, maxCount={max_count}")
        fallback = [0]
    
    if call_count <= 20:
        print(f"Call {call_count}: type={sel_type}, ctx={sel_ctx}, opts={len(options)}, maxCount={max_count}, returning={fallback}")
    
    return fallback

env = make("cabt", debug=True)
result = env.run([debug_agent, debug_agent])

print("\n--- Results ---")
found_error = False
for step_idx, step in enumerate(env.steps):
    for player_idx, player_data in enumerate(step):
        err = player_data.get("error")
        status = player_data.get("status")
        if status == "ERROR" or err:
            print("Step %d, Player %d: ERROR - %s" % (step_idx, player_idx, err))
            found_error = True
            break
    if found_error:
        break

if not found_error:
    r0 = env.steps[-1][0].get("reward")
    r1 = env.steps[-1][1].get("reward")
    print("Game completed: P0=%s, P1=%s, steps=%d" % (r0, r1, len(env.steps)))

os.chdir("..")
