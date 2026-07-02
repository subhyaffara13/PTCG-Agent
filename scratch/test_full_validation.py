import sys
import os
from pathlib import Path

script_dir = Path(__file__).parent.resolve()
workspace_dir = script_dir.parent
sys.path.insert(0, str(workspace_dir))
# Running from root so relative paths work and pyright resolves modules


from kaggle_environments import make

# Test 1: Use the actual main.py agent
print("=== Test 1: Full main.py agent ===")
try:
    from submission.main import agent
    env = make("cabt", debug=True)
    result = env.run([agent, agent])
    
    found_error = False
    for step_idx, step in enumerate(env.steps):
        for player_idx, player_data in enumerate(step):
            err = player_data.get("error")
            status = player_data.get("status")
            if status == "ERROR" or err:
                print("Step %d, Player %d: %s - %s" % (step_idx, player_idx, status, err))
                found_error = True
                break
        if found_error:
            break
    
    if not found_error:
        r0 = env.steps[-1][0].get("reward")
        r1 = env.steps[-1][1].get("reward")
        print("OK: %d steps, P0=%s, P1=%s" % (len(env.steps), r0, r1))
except Exception as e:
    import traceback
    traceback.print_exc()

# Test 2: Test against the default random agent
print("\n=== Test 2: main.py vs random ===")
try:
    env2 = make("cabt", debug=True)
    result2 = env2.run([agent, "random"])
    
    found_error = False
    for step_idx, step in enumerate(env2.steps):
        for player_idx, player_data in enumerate(step):
            err = player_data.get("error")
            status = player_data.get("status")
            if status == "ERROR" or err:
                print("Step %d, Player %d: %s - %s" % (step_idx, player_idx, status, err))
                found_error = True
                break
        if found_error:
            break
    
    if not found_error:
        r0 = env2.steps[-1][0].get("reward")
        r1 = env2.steps[-1][1].get("reward")
        print("OK: %d steps, P0=%s, P1=%s" % (len(env2.steps), r0, r1))
except Exception as e:
    import traceback
    traceback.print_exc()

# Test 3: Run multiple games to catch intermittent errors
print("\n=== Test 3: 5 games for reliability ===")
errors = 0
for game_num in range(5):
    try:
        env3 = make("cabt", debug=True)
        result3 = env3.run([agent, "random"])
        
        for step in env3.steps:
            for p in [0, 1]:
                if step[p].get("status") == "ERROR" or step[p].get("error"):
                    errors += 1
                    print("Game %d: ERROR at step" % game_num)
                    break
            else:
                continue
            break
        else:
            r = env3.steps[-1][0].get("reward")
            print("Game %d: OK (%d steps, result=%s)" % (game_num, len(env3.steps), r))
    except Exception as e:
        errors += 1
        print("Game %d: EXCEPTION - %s" % (game_num, str(e)[:100]))

print("\nTotal errors: %d/5" % errors)
