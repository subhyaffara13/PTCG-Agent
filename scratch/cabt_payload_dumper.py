import os
import json
from kaggle_environments import make

os.environ["FAST_SIM_MODE"] = "true"
env = make("cabt")

dump = []

def dumper_agent(obs):
    turn = obs.get("current", {}).get("turn", 0)
    sel = obs.get("select")
    
    # Save the raw observation for analysis
    if sel:
        dump.append({
            "turn": turn,
            "select_type": sel.get("type"),
            "select_context": sel.get("context"),
            "options": sel.get("option", [])
        })
    
    if sel is None:
        # initial deck loading
        # Providing a standard 60-card list of ints
        deck = [
            721, 721, 722, 722, 722, 722, 723, 723, 723, 723,
            1092, 1121, 1121, 1145, 1145, 1163, 1163, 1219,
            1219, 1219, 1219, 1227, 1227, 1227, 1227, 1262,
            1262, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3
        ]
        return deck
        
    return [0]  # blindly select first option

# Run a quick 10-step simulation
print("Starting simulation...")
steps = env.run([dumper_agent, dumper_agent])
print(f"Simulation ended after {len(steps)} steps.")

with open("logs/debug_payload_dump.json", "w") as f:
    json.dump(dump, f, indent=2)
print("Dumped payloads to logs/debug_payload_dump.json")
