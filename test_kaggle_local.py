from kaggle_environments import make

deck = [318, 6, 6, 6, 6, 6, 6, 6, 6, 304, 193, 1040, 62, 226, 1033, 320, 320, 191, 336, 345, 244, 340, 3, 872, 1031, 419, 894, 949, 949, 623, 806, 513, 25, 460, 330, 121, 932, 5, 386, 854, 326, 756, 16, 407, 992, 133, 868, 723, 832, 332, 328, 1016, 975, 302, 82, 82, 452, 1062, 991, 44]

def agent(obs, config):
    if obs.select is None:
        return deck
    return [0]

env = make("cabt", debug=True)
env.run([agent, agent])
print("Step 0 error:", env.steps[0][0].get('error', 'None'))
