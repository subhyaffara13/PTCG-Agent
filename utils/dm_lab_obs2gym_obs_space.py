
def dm_lab_obs2gym_obs_space(observation: dict) -> spaces.Space[Any]:
    """Gets the observation spec from a single observation."""
    assert isinstance(
        observation, (OrderedDict, dict)
    ), f"Observation must be a dict, got {observation}"

    all_spaces = dict()
    for key, value in observation.items():
        dtype = value.dtype

        low = None
        high = None
        if np.issubdtype(dtype, np.integer):
            low = np.iinfo(dtype).min
            high = np.iinfo(dtype).max
        elif np.issubdtype(dtype, np.inexact):
            low = float("-inf")
            high = float("inf")
        else:
            raise ValueError(f"Unknown dtype {dtype}.")

        all_spaces[key] = spaces.Box(low=low, high=high, shape=value.shape, dtype=dtype)

    return spaces.Dict(all_spaces)

