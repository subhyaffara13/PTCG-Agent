
def minatar_action_map(action_jax: int, env_name: str):
    """Helper that maps gymnax MinAtar action to the numpy equivalent."""
    all_actions = ["n", "l", "u", "r", "d", "f"]
    if env_name == "Asterix-MinAtar":
        minimal_actions = ["n", "l", "u", "r", "d"]
    elif env_name == "Breakout-MinAtar":
        minimal_actions = ["n", "l", "r"]
    elif env_name == "Freeway-MinAtar":
        minimal_actions = ["n", "u", "d"]
    elif env_name == "Seaquest-MinAtar":
        minimal_actions = ["n", "l", "u", "r", "d", "f"]
    elif env_name == "SpaceInvaders-MinAtar":
        minimal_actions = ["n", "l", "r", "f"]
    else:
        raise ValueError(f"{env_name} not in implemented MinAtar environments.")
    action_idx = all_actions.index(minimal_actions[action_jax])
    return action_idx

