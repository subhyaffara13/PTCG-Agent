
def batch_space(space: Space[Any], n: int = 1) -> Space[Any]:
    """Batch spaces of size `n` optimized for neural networks.

    Args:
        space: Space (e.g. the observation space for a single environment in the vectorized environment).
        n: Number of spaces to batch by (e.g. the number of environments in a vectorized environment).

    Returns:
        Batched space of size `n`.

    Raises:
        ValueError: Cannot batch spaces that does not have a registered function.

    Example:

        >>> from gymnasium.spaces import Box, Dict
        >>> import numpy as np
        >>> space = Dict({
        ...     'position': Box(low=0, high=1, shape=(3,), dtype=np.float32),
        ...     'velocity': Box(low=0, high=1, shape=(2,), dtype=np.float32)
        ... })
        >>> batch_space(space, n=5)
        Dict('position': Box(0.0, 1.0, (5, 3), float32), 'velocity': Box(0.0, 1.0, (5, 2), float32))
    """
    raise TypeError(
        f"The space provided to `batch_space` is not a gymnasium Space instance, type: {type(space)}, {space}"
    )


def batch_space(space: Space, n: int = 1) -> Space:
    """Create a (batched) space, containing multiple copies of a single space.

    Example::

        >>> from gym.spaces import Box, Dict
        >>> space = Dict({
        ...     'position': Box(low=0, high=1, shape=(3,), dtype=np.float32),
        ...     'velocity': Box(low=0, high=1, shape=(2,), dtype=np.float32)
        ... })
        >>> batch_space(space, n=5)
        Dict(position:Box(5, 3), velocity:Box(5, 2))

    Args:
        space: Space (e.g. the observation space) for a single environment in the vectorized environment.
        n: Number of environments in the vectorized environment.

    Returns:
        Space (e.g. the observation space) for a batch of environments in the vectorized environment.

    Raises:
        ValueError: Cannot batch space that is not a valid :class:`gym.Space` instance
    """
    raise ValueError(
        f"Cannot batch space with type `{type(space)}`. The space must be a valid `gym.Space` instance."
    )

