import sys
from pathlib import Path

# Verify Python 3.11 compatibility before running local match
from utils.verify_compatibility import verify_compatibility

verify_compatibility(Path("submission"))

# Add submission directory to sys.path to resolve internal cb_agents/router imports
sub_path = str(Path(__file__).parent / "submission")
if sub_path not in sys.path:
    sys.path.insert(0, sub_path)

from kaggle_environments import make
from main import agent

env = make("cabt", debug=True)
env.run([agent, agent])
print("Step 0 error:", env.steps[0][0].get('error', 'None'))
print("Game steps count:", len(env.steps))
print("Game finished. Status P1:", env.state[0].status, "Status P2:", env.state[1].status)
if env.state[0].status == "ERROR":
    print("P1 error detail:", env.steps[-1][0].get('error'))
if env.state[1].status == "ERROR":
    print("P2 error detail:", env.steps[-1][1].get('error'))
