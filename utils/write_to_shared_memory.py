
def write_to_shared_memory(
    space: Space,
    index: int,
    value: np.ndarray,
    shared_memory: dict[str, Any] | tuple[Any, ...] | SynchronizedArray,
):
    """Write the observation of a single environment into shared memory.

    Args:
        space: Observation space of a single environment in the vectorized environment.
        index: Index of the environment (must be in `[0, num_envs)`).
        value: Observation of the single environment to write to shared memory.
        shared_memory: Shared object across processes. This contains the observations from the vectorized environment.
            This object is created with `create_shared_memory`.

    Raises:
        CustomSpaceError: Space is not a valid :class:`gymnasium.Space` instance
    """
    if isinstance(space, Space):
        raise CustomSpaceError(
            f"Space of type `{type(space)}` doesn't have an registered `write_to_shared_memory` function. Register `{type(space)}` for `write_to_shared_memory` to support it."
        )
    else:
        raise TypeError(
            f"The space provided to `write_to_shared_memory` is not a gymnasium Space instance, type: {type(space)}, {space}"
        )


def write_to_shared_memory(
    space: Space,
    index: int,
    value: np.ndarray,
    shared_memory: Union[dict, tuple, mp.Array],
):
    """Write the observation of a single environment into shared memory.

    Args:
        space: Observation space of a single environment in the vectorized environment.
        index: Index of the environment (must be in `[0, num_envs)`).
        value: Observation of the single environment to write to shared memory.
        shared_memory: Shared object across processes. This contains the observations from the vectorized environment.
            This object is created with `create_shared_memory`.

    Raises:
        CustomSpaceError: Space is not a valid :class:`gym.Space` instance
    """
    raise CustomSpaceError(
        "Cannot write to a shared memory for space with "
        f"type `{type(space)}`. Shared memory only supports "
        "default Gym spaces (e.g. `Box`, `Tuple`, "
        "`Dict`, etc...), and does not support custom "
        "Gym spaces."
    )

