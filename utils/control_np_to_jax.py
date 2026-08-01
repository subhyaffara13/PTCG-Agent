
def control_np_to_jax(env, env_name: str = "Pendulum-v1", get_jax: bool = False):
    """Collects env state of classic_control into dict for JAX `step`."""
    state_gym_to_jax = None
    if env_name == "Pendulum-v1":
        state_gym_to_jax = {
            "theta": env.state[0],
            "theta_dot": env.state[1],
            "last_u": env.last_u,
            "time": 0,
        }
        if get_jax:
            return pendulum.EnvState(**state_gym_to_jax)
    elif env_name == "CartPole-v1":
        state_gym_to_jax = {
            "x": env.state[0],
            "x_dot": env.state[1],
            "theta": env.state[2],
            "theta_dot": env.state[3],
            "time": 0,
        }
        if get_jax:
            return cartpole.EnvState(**state_gym_to_jax)
    elif env_name == "MountainCar-v0":
        state_gym_to_jax = {
            "position": env.state[0],
            "velocity": env.state[1],
            "time": 0,
        }
        if get_jax:
            return mountain_car.EnvState(**state_gym_to_jax)
    elif env_name == "MountainCarContinuous-v0":
        state_gym_to_jax = {
            "position": env.state[0],
            "velocity": env.state[1],
            "time": 0,
        }
        if get_jax:

            return continuous_mountain_car.EnvState(**state_gym_to_jax)
    elif env_name == "Acrobot-v1":

        state_gym_to_jax = {
            "joint_angle1": env.state[0],
            "joint_angle2": env.state[1],
            "velocity_1": env.state[2],
            "velocity_2": env.state[3],
            "time": 0,
        }
        if get_jax:

            return acrobot.EnvState(**state_gym_to_jax)
    return state_gym_to_jax

