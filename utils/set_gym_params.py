
def set_gym_params(gym_env, env_name, params):
    """Set gym environment parameters."""
    if env_name == "Acrobot-v1":
        gym_env.env.LINK_LENGTH_1 = params.link_length_1
        gym_env.env.LINK_LENGTH_2 = params.link_length_2
    elif env_name == "CartPole-v1":
        gym_env.env.x_threshold = params.x_threshold
        gym_env.env.length = params.length
    elif env_name == "Pendulum-v1":
        pass
    elif env_name == "MountainCar-v0":
        gym_env.env.max_position = params.max_position
        gym_env.env.min_position = params.min_position
        gym_env.env.goal_position = params.goal_position
    elif env_name == "MountainCarContinuous-v0":
        gym_env.env.max_position = params.max_position
        gym_env.env.min_position = params.min_position
        gym_env.env.goal_position = params.goal_position
    return

