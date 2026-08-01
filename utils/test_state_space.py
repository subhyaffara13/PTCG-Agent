
def test_state_space(env):
    assert isinstance(
        env.state_space, gymnasium.spaces.Space
    ), "State space for each environment must extend gymnasium.spaces.Space"
    if not (
        isinstance(env.state_space, gymnasium.spaces.Box)
        or isinstance(env.state_space, gymnasium.spaces.Discrete)
    ):
        warnings.warn(
            "State space for each environment probably should be gymnasium.spaces.box or gymnasium.spaces.discrete"
        )

    if isinstance(env.state_space, gymnasium.spaces.Box):
        if (
            np.any(np.equal(env.state_space.low, -np.inf))
            and str(env.unwrapped) not in env_neg_inf_state
        ):
            warnings.warn(
                "Environment's minimum state space value is -infinity. This is probably too low."
            )
        if (
            np.any(np.equal(env.state_space.high, np.inf))
            and str(env.unwrapped) not in env_pos_inf_state
        ):
            warnings.warn(
                "Environment's maximum state space value is infinity. This is probably too high"
            )
        if np.any(np.equal(env.state_space.low, env.state_space.high)):
            warnings.warn(
                "Environment's maximum and minimum state space values are equal"
            )
        if np.any(np.greater(env.state_space.low, env.state_space.high)):
            assert (
                False
            ), "Environment's minimum state space value is greater than it's maximum"
        if env.state_space.low.shape != env.state_space.shape:
            assert (
                False
            ), "Environment's state_space.low and state_space have different shapes"
        if env.state_space.high.shape != env.state_space.shape:
            assert (
                False
            ), "Environment's state_space.high and state_space have different shapes"

