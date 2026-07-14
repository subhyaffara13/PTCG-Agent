import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.resolve().parent))

from kaggle_environments import make
from submission.main import agent

def run_match():
    env = make("cabt", debug=True)
    env.run([agent, "random"])
    
    print(f"Match finished in {len(env.steps)} steps.")
    for step_idx, step in enumerate(env.steps):
        p0 = step[0]
        obs = p0.get("observation", {})
        action = p0.get("action")
        status = p0.get("status")
        reward = p0.get("reward")
        print(f"Step {step_idx}: Status: {status}, Action: {action}")
        if status == "ERROR":
            print(f"ERROR: {p0.get('error')}")

if __name__ == "__main__":
    run_match()
