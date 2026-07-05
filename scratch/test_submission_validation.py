"""Test submission against kaggle cabt environment to find validation errors."""
import sys
import os
import traceback

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'submission')))
os.chdir(os.path.join(os.path.dirname(__file__), '..', 'submission'))

import os
os.environ["KAGGLE_KERNEL_RUN_TYPE"] = "Interactive"

try:
    from kaggle_environments import make
    from main import agent, DEFAULT_DECK

    env = make("cabt", debug=True)
    result = env.run([agent, agent])

    found_error = False
    for step_idx, step in enumerate(env.steps):
        for player_idx, player_data in enumerate(step):
            err = player_data.get("error")
            status = player_data.get("status")
            if status == "ERROR" or err:
                print(f"Step {step_idx}, Player {player_idx}: ERROR")
                print(f"  Error: {err}")
                print(f"  Status: {status}")
                found_error = True
                break
        if found_error:
            break

    if not found_error:
        num_steps = len(env.steps)
        p0_reward = env.steps[-1][0].get("reward", "?")
        p1_reward = env.steps[-1][1].get("reward", "?")
        print(f"All {num_steps} steps completed successfully!")
        print(f"Final scores: P0={p0_reward}, P1={p1_reward}")

except Exception as e:
    traceback.print_exc()
finally:
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
