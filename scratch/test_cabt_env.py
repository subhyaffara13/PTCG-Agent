import sys
from pathlib import Path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))
sys.path.insert(0, str(workspace_root / "submission"))

# Force HAS_CPP = False to simulate Kaggle Linux environment without C++ binary
import cb_agents.mcts_engine
cb_agents.mcts_engine.HAS_CPP = False

from main import agent

print("Running local CABT simulation with HAS_CPP=False (simulating Kaggle Linux)...")
from kaggle_environments import make
env = make("cabt", debug=True)
env.run([agent, agent])

print("Simulation finished. Steps run:", len(env.steps))
errors = []
for i, step in enumerate(env.steps):
    for player_idx, p_state in enumerate(step):
        err = p_state.get('error')
        if err:
            errors.append((i, player_idx, err))

if errors:
    print("Errors detected during simulation:")
    for step_idx, p_idx, err in errors:
        print(f"  Step {step_idx}, Player {p_idx}: {err}")
else:
    print("Simulation completed with zero errors!")
