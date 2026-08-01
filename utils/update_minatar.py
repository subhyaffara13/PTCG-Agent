
def update_minatar(im, env, state):
    """Update the Minatar visualization."""
    obs = env.get_obs(state)
    n_channels = env.obs_shape[-1]
    numerical_state = (
        np.amax(obs * np.reshape(np.arange(n_channels) + 1, (1, 1, -1)), 2) + 0.5
    )
    im.set_data(numerical_state)

