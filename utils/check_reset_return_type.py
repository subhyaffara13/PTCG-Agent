
def check_reset_return_type(env: gym.Env):
    """Checks that :meth:`reset` correctly returns a tuple of the form `(obs , info)`.

    Args:
        env: The environment to check
    Raises:
        AssertionError depending on spec violation
    """
    result = env.reset()
    assert isinstance(
        result, tuple
    ), f"The result returned by `env.reset()` was not a tuple of the form `(obs, info)`, where `obs` is a observation and `info` is a dictionary containing additional information. Actual type: `{type(result)}`"
    assert (
        len(result) == 2
    ), f"Calling the reset method did not return a 2-tuple, actual length: {len(result)}"

    obs, info = result
    assert (
        obs in env.observation_space
    ), "The first element returned by `env.reset()` is not within the observation space."
    assert isinstance(
        info, dict
    ), f"The second element returned by `env.reset()` was not a dictionary, actual type: {type(info)}"


def check_reset_return_type(env: gym.Env):
    """Checks that :meth:`reset` correctly returns a tuple of the form `(obs , info)`.

    Args:
        env: The environment to check
    Raises:
        AssertionError depending on spec violation
    """
    result = env.reset()
    assert isinstance(
        result, tuple
    ), f"The result returned by `env.reset()` was not a tuple of the form `(obs, info)`, where `obs` is a observation and `info` is a dictionary containing additional information. Actual type: `{type(result)}`"
    assert (
        len(result) == 2
    ), f"Calling the reset method did not return a 2-tuple, actual length: {len(result)}"

    obs, info = result
    assert (
        obs in env.observation_space
    ), "The first element returned by `env.reset()` is not within the observation space."
    assert isinstance(
        info, dict
    ), f"The second element returned by `env.reset()` was not a dictionary, actual type: {type(info)}"

