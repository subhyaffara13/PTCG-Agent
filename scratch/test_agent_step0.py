import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'submission')))
os.chdir(os.path.join(os.path.dirname(__file__), '..', 'submission'))

from main import agent, get_val
from kaggle_environments import make

print("Defining inspector agent...")
step_counter = 0

def inspector_agent(obs, config):
    global step_counter
    print("--- STEP CALL ---")
    print("obs type:", type(obs))
    print("obs keys/attributes:", [k for k in dir(obs) if not k.startswith('_')])
    print("obs select:", getattr(obs, "select", None))
    print("obs step:", getattr(obs, "step", None))
    
    val = agent(obs, config)
    print("Agent returned:", val)
    
    step_counter += 1
    if step_counter >= 4:
        print("Stopping early to avoid long output.")
        sys.exit(0)
    return val


env = make("cabt", debug=True)
env.run([inspector_agent, inspector_agent])
print("Steps completed.")
