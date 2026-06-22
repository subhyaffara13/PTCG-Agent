
def agent(obs, config):
    step = obs.step if hasattr(obs, 'step') else (obs.get('step', 0) if isinstance(obs, dict) else 0)
    if step == 0:
        return [
            721, 721, 722, 722, 722, 722, 723, 723, 723, 723,
            1092, 1121, 1121, 1145, 1145, 1163, 1163, 1219,
            1219, 1219, 1219, 1227, 1227, 1227, 1227, 1262,
            1262, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3
        ]
    return [0]
