
def filter_actions(state, env):
    enable_annotations = env.configuration["annotations"]
    if not enable_annotations:
        for team in range(len(state)):
            filtered = []
            if state[team] is not None and state[team].action is not None:
                for l in state[team].action:
                    if len(l) > 0 and l[0] != "d":
                        filtered.append(l)
                state[team].action = filtered

