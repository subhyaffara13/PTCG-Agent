
def dm_obs2gym_obs(obs) -> np.ndarray | dict[str, Any]:
    """Converts a dm_env observation to a gymnasium observation.

    Array observations are converted to numpy arrays. Dict observations are converted recursively per key.

    Args:
        obs: The dm_env observation

    Returns:
        The Gymnasium-compatible observation.
    """
    if isinstance(obs, (OrderedDict, dict)):
        return {key: dm_obs2gym_obs(value) for key, value in copy.copy(obs).items()}
    else:
        return np.asarray(obs)

