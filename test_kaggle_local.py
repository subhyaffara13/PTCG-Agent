from kaggle_environments import make
from submission import agent

env = make("cabt", debug=True)
env.run([agent, agent])
print("Step 0 error:", env.steps[0][0].get('error', 'None'))
print("Game steps count:", len(env.steps))
print("Game finished. Status P1:", env.state[0].status, "Status P2:", env.state[1].status)
if env.state[0].status == "ERROR":
    print("P1 error detail:", env.steps[-1][0].get('error'))
if env.state[1].status == "ERROR":
    print("P2 error detail:", env.steps[-1][1].get('error'))
