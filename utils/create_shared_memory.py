
def create_shared_memory(
    space: Space[Any], n: int = 1, ctx=mp
) -> dict[str, Any] | tuple[Any, ...] | SynchronizedArray:
    """Create a shared memory object, to be shared across processes.

    This eventually contains the observations from the vectorized environment.

    Args:
        space: Observation space of a single environment in the vectorized environment.
        n: Number of environments in the vectorized environment (i.e. the number of processes).
        ctx: The multiprocess module

    Returns:
        shared_memory for the shared object across processes.

    Raises:
        CustomSpaceError: Space is not a valid :class:`gymnasium.Space` instance
    """
    if isinstance(space, Space):
        raise CustomSpaceError(
            f"Space of type `{type(space)}` doesn't have an registered `create_shared_memory` function. Register `{type(space)}` for `create_shared_memory` to support it."
        )
    else:
        raise TypeError(
            f"The space provided to `create_shared_memory` is not a gymnasium Space instance, type: {type(space)}, {space}"
        )


def create_shared_memory(
    space: Space, n: int = 1, ctx=mp
) -> Union[dict, tuple, mp.Array]:
    """Create a shared memory object, to be shared across processes.

    This eventually contains the observations from the vectorized environment.

    Args:
        space: Observation space of a single environment in the vectorized environment.
        n: Number of environments in the vectorized environment (i.e. the number of processes).
        ctx: The multiprocess module

    Returns:
        shared_memory for the shared object across processes.

    Raises:
        CustomSpaceError: Space is not a valid :class:`gym.Space` instance
    """
    raise CustomSpaceError(
        "Cannot create a shared memory for space with "
        f"type `{type(space)}`. Shared memory only supports "
        "default Gym spaces (e.g. `Box`, `Tuple`, "
        "`Dict`, etc...), and does not support custom "
        "Gym spaces."
    )

