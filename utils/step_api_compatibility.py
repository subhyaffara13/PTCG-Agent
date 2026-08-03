from typing import Union

def step_api_compatibility(
    step_returns: TerminatedTruncatedStepType | DoneStepType,
    output_truncation_bool: bool = True,
    is_vector_env: bool = False,
) -> TerminatedTruncatedStepType | DoneStepType:
    """Function to transform step returns to the API specified by ``output_truncation_bool``.

    .. py:currentmodule:: gymnasium.Env

    Done (old) step API refers to :meth:`step` method returning ``(observation, reward, done, info)``
    Terminated Truncated (new) step API refers to :meth:`step` method returning ``(observation, reward, terminated, truncated, info)``
    (Refer to docs for details on the API change)

    Args:
        step_returns (tuple): Items returned by :meth:`step`. Can be ``(obs, rew, done, info)`` or ``(obs, rew, terminated, truncated, info)``
        output_truncation_bool (bool): Whether the output should return two booleans (new API) or one (old) (``True`` by default)
        is_vector_env (bool): Whether the ``step_returns`` are from a vector environment

    Returns:
        step_returns (tuple): Depending on ``output_truncation_bool``, it can return ``(obs, rew, done, info)`` or ``(obs, rew, terminated, truncated, info)``

    Example:
        This function can be used to ensure compatibility in step interfaces with conflicting API. E.g. if env is written in old API,
        wrapper is written in new API, and the final step output is desired to be in old API.

        >>> import gymnasium as gym
        >>> env = gym.make("CartPole-v0")
        >>> _, _ = env.reset()
        >>> obs, reward, done, info = step_api_compatibility(env.step(0), output_truncation_bool=False)
        >>> obs, reward, terminated, truncated, info = step_api_compatibility(env.step(0), output_truncation_bool=True)

        >>> vec_env = gym.make_vec("CartPole-v0", vectorization_mode="sync")
        >>> _, _ = vec_env.reset()
        >>> obs, rewards, dones, infos = step_api_compatibility(vec_env.step([0]), is_vector_env=True, output_truncation_bool=False)
        >>> obs, rewards, terminations, truncations, infos = step_api_compatibility(vec_env.step([0]), is_vector_env=True, output_truncation_bool=True)

    """
    if output_truncation_bool:
        return convert_to_terminated_truncated_step_api(step_returns, is_vector_env)
    else:
        return convert_to_done_step_api(step_returns, is_vector_env)


def step_api_compatibility(
    step_returns: Union[TerminatedTruncatedStepType, DoneStepType],
    output_truncation_bool: bool = True,
    is_vector_env: bool = False,
) -> Union[TerminatedTruncatedStepType, DoneStepType]:
    """Function to transform step returns to the API specified by `output_truncation_bool` bool.

    Done (old) step API refers to step() method returning (observation, reward, done, info)
    Terminated Truncated (new) step API refers to step() method returning (observation, reward, terminated, truncated, info)
    (Refer to docs for details on the API change)

    Args:
        step_returns (tuple): Items returned by step(). Can be (obs, rew, done, info) or (obs, rew, terminated, truncated, info)
        output_truncation_bool (bool): Whether the output should return two booleans (new API) or one (old) (True by default)
        is_vector_env (bool): Whether the step_returns are from a vector environment

    Returns:
        step_returns (tuple): Depending on `output_truncation_bool` bool, it can return (obs, rew, done, info) or (obs, rew, terminated, truncated, info)

    Examples:
        This function can be used to ensure compatibility in step interfaces with conflicting API. Eg. if env is written in old API,
         wrapper is written in new API, and the final step output is desired to be in old API.

        >>> obs, rew, done, info = step_api_compatibility(env.step(action), output_truncation_bool=False)
        >>> obs, rew, terminated, truncated, info = step_api_compatibility(env.step(action), output_truncation_bool=True)
        >>> observations, rewards, dones, infos = step_api_compatibility(vec_env.step(action), is_vector_env=True)
    """
    if output_truncation_bool:
        return convert_to_terminated_truncated_step_api(step_returns, is_vector_env)
    else:
        return convert_to_done_step_api(step_returns, is_vector_env)

