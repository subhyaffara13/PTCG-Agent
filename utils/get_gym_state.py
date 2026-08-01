
def get_gym_state(state, env_name):
    """Get gym environment state."""
    if env_name == "Acrobot-v1":
        return np.array(
            [
                state.joint_angle1,
                state.joint_angle2,
                state.velocity_1,
                state.velocity_2,
            ]
        )
    elif env_name == "CartPole-v1":
        return np.array([state.x, state.x_dot, state.theta, state.theta_dot])
    elif env_name == "Pendulum-v1":
        return np.array([state.theta, state.theta_dot, state.last_u])
    elif env_name == "MountainCar-v0":
        return np.array([state.position, state.velocity])
    elif env_name == "MountainCarContinuous-v0":
        return np.array([state.position, state.velocity])

