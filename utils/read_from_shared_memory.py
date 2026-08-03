from typing import Any, Union

def read_from_shared_memory(
    space: Space, shared_memory: dict | tuple | SynchronizedArray, n: int = 1
) -> dict[str, Any] | tuple[Any, ...] | np.ndarray:
    """Read the batch of observations from shared memory as a numpy array.

    ..notes::
        The numpy array objects returned by `read_from_shared_memory` shares the
        memory of `shared_memory`. Any changes to `shared_memory` are forwarded
        to `observations`, and vice-versa. To avoid any side-effect, use `np.copy`.

    Args:
        space: Observation space of a single environment in the vectorized environment.
        shared_memory: Shared object across processes. This contains the observations from the vectorized environment.
            This object is created with `create_shared_memory`.
        n: Number of environments in the vectorized environment (i.e. the number of processes).

    Returns:
        Batch of observations as a (possibly nested) numpy array.

    Raises:
        CustomSpaceError: Space is not a valid :class:`gymnasium.Space` instance
    """
    if isinstance(space, Space):
        raise CustomSpaceError(
            f"Space of type `{type(space)}` doesn't have an registered `read_from_shared_memory` function. Register `{type(space)}` for `read_from_shared_memory` to support it."
        )
    else:
        raise TypeError(
            f"The space provided to `read_from_shared_memory` is not a gymnasium Space instance, type: {type(space)}, {space}"
        )


def read_from_shared_memory(
    space: Space, shared_memory: Union[dict, tuple, mp.Array], n: int = 1
) -> Union[dict, tuple, np.ndarray]:
    """Read the batch of observations from shared memory as a numpy array.

    ..notes::
        The numpy array objects returned by `read_from_shared_memory` shares the
        memory of `shared_memory`. Any changes to `shared_memory` are forwarded
        to `observations`, and vice-versa. To avoid any side-effect, use `np.copy`.

    Args:
        space: Observation space of a single environment in the vectorized environment.
        shared_memory: Shared object across processes. This contains the observations from the vectorized environment.
            This object is created with `create_shared_memory`.
        n: Number of environments in the vectorized environment (i.e. the number of processes).

    Returns:
        Batch of observations as a (possibly nested) numpy array.

    Raises:
        CustomSpaceError: Space is not a valid :class:`gym.Space` instance
    """
    raise CustomSpaceError(
        "Cannot read from a shared memory for space with "
        f"type `{type(space)}`. Shared memory only supports "
        "default Gym spaces (e.g. `Box`, `Tuple`, "
        "`Dict`, etc...), and does not support custom "
        "Gym spaces."
    )

