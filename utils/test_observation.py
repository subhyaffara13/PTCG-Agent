
def test_observation(observation, observation_0, env_name=None):
    if not isinstance(observation, np.ndarray):
        if env_name is not None and env_name not in env_obs_dicts:
            warnings.warn("Observation is not a NumPy array")
        if isinstance(observation, dict) and "observation" in observation.keys():
            observation = observation["observation"]
            test_observation(observation, observation_0, env_name)
        if isinstance(observation, dict) and "action_mask" in observation.keys():
            test_action_mask(observation["action_mask"], env_name)
        return
    if np.isinf(observation).any():
        warnings.warn(
            "Observation contains infinity (np.inf) or negative infinity (-np.inf)"
        )
    if np.isnan(observation).any():
        warnings.warn("Observation contains NaNs")
    if len(observation.shape) > 3:
        warnings.warn("Observation has more than 3 dimensions")
    if observation.shape == (0,):
        assert False, "Observation can not be an empty array"
    if observation.shape == (1,):
        warnings.warn("Observation is a single number")
    if not isinstance(observation, observation_0.__class__):
        warnings.warn("Observations between agents are different classes")
    if (
        (observation.shape != observation_0.shape)
        and (len(observation.shape) == len(observation_0.shape))
        and env_name not in env_diff_obs_shapes
    ):
        warnings.warn("Observations are different shapes")
    if len(observation.shape) != len(observation_0.shape):
        warnings.warn("Observations have different number of dimensions")
    if not np.can_cast(observation.dtype, np.dtype("float64")):
        warnings.warn("Observation numpy array is not a numeric dtype")
    if (
        np.array_equal(observation, np.zeros(observation.shape))
        and env_name not in env_all_zeros_obs
    ):
        warnings.warn("Observation numpy array is all zeros.")
    if (
        not np.all(observation >= 0)
        and (
            (len(observation.shape) == 2)
            or (len(observation.shape) == 3 and observation.shape[2] == 1)
            or (len(observation.shape) == 3 and observation.shape[2] == 3)
        )
        and env_name not in env_graphical_obs
    ):
        warnings.warn(
            "The observation contains negative numbers and is in the shape of a graphical observation. This might be a bad thing."
        )

