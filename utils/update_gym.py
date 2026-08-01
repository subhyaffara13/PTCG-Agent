
def update_gym(im, env, state):
    """Update gym environment."""
    if env.name == "Pendulum-v1":
        gym_env = gym.make("Pendulum-v0")
    else:
        gym_env = gym.make(env.name)
    gym_state = get_gym_state(state, env.name)
    if env.name == "Pendulum-v1":
        gym_env.env.last_u = gym_state[-1]
    gym_env.env.state = gym_state
    rgb_array = gym_env.render(mode="rgb_array")
    im.set_data(rgb_array)
    gym_env.close()
    return im

