from typing import Any, Callable, Union

def create_empty_array(
    space: Space, n: int = 1, fn: Callable = np.zeros
) -> tuple[Any, ...] | dict[str, Any] | np.ndarray:
    """Create an empty (possibly nested and normally numpy-based) array, used in conjunction with ``concatenate(..., out=array)``.

    In most cases, the array will be contained within the batched space, however, this is not guaranteed.

    Args:
        space: Observation space of a single environment in the vectorized environment.
        n: Number of environments in the vectorized environment. If ``None``, creates an empty sample from ``space``.
        fn: Function to apply when creating the empty numpy array. Examples of such functions are ``np.empty`` or ``np.zeros``.

    Returns:
        The output object. This object is a (possibly nested) numpy array.

    Raises:
        ValueError: Space is not a valid :class:`gymnasium.Space` instance

    Example:
        >>> from gymnasium.spaces import Box, Dict
        >>> import numpy as np
        >>> space = Dict({
        ... 'position': Box(low=0, high=1, shape=(3,), dtype=np.float32),
        ... 'velocity': Box(low=0, high=1, shape=(2,), dtype=np.float32)})
        >>> create_empty_array(space, n=2, fn=np.zeros)
        {'position': array([[0., 0., 0.],
               [0., 0., 0.]], dtype=float32), 'velocity': array([[0., 0.],
               [0., 0.]], dtype=float32)}
    """
    raise TypeError(
        f"The space provided to `create_empty_array` is not a gymnasium Space instance, type: {type(space)}, {space}"
    )


def create_empty_array(
    space: Space, n: int = 1, fn: callable = np.zeros
) -> Union[tuple, dict, np.ndarray]:
    """Create an empty (possibly nested) numpy array.

    Example::

        >>> from gym.spaces import Box, Dict
        >>> space = Dict({
        ... 'position': Box(low=0, high=1, shape=(3,), dtype=np.float32),
        ... 'velocity': Box(low=0, high=1, shape=(2,), dtype=np.float32)})
        >>> create_empty_array(space, n=2, fn=np.zeros)
        OrderedDict([('position', array([[0., 0., 0.],
                                         [0., 0., 0.]], dtype=float32)),
                     ('velocity', array([[0., 0.],
                                         [0., 0.]], dtype=float32))])

    Args:
        space: Observation space of a single environment in the vectorized environment.
        n: Number of environments in the vectorized environment. If `None`, creates an empty sample from `space`.
        fn: Function to apply when creating the empty numpy array. Examples of such functions are `np.empty` or `np.zeros`.

    Returns:
        The output object. This object is a (possibly nested) numpy array.

    Raises:
        ValueError: Space is not a valid :class:`gym.Space` instance
    """
    raise ValueError(
        f"Space of type `{type(space)}` is not a valid `gym.Space` instance."
    )

