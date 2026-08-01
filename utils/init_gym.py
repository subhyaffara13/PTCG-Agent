
def init_gym(ax, env, state, params):
    """Initialize gym environment."""
    if env.name == "Pendulum-v1":
        gym_env = gym.make("Pendulum-v0")
    else:
        gym_env = gym.make(env.name)
    gym_env.reset()
    set_gym_params(gym_env, env.name, params)
    gym_state = get_gym_state(state, env.name)
    if env.name == "Pendulum-v1":
        gym_env.env.last_u = gym_state[-1]
    gym_env.env.state = gym_state
    rgb_array = gym_env.render(mode="rgb_array")
    ax.set_xticks([])
    ax.set_yticks([])
    gym_env.close()
    return ax.imshow(rgb_array)

