
def flatten_space(space: Space[Any]) -> Box | Dict | Sequence | Tuple | Graph:
    """Flatten a space into a space that is as flat as possible.

    This function will attempt to flatten ``space`` into a single :class:`gymnasium.spaces.Box` space.
    However, this might not be possible when ``space`` is an instance of :class:`gymnasium.spaces.Graph`,
    :class:`gymnasium.spaces.Sequence` or a compound space that contains a :class:`gymnasium.spaces.Graph`
    or :class:`gymnasium.spaces.Sequence` space.
    This is equivalent to :func:`flatten`, but operates on the space itself. The
    result for non-graph spaces is always a :class:`gymnasium.spaces.Box` with flat boundaries. While
    the result for graph spaces is always a :class:`gymnasium.spaces.Graph` with
    :attr:`Graph.node_space` being a ``Box``
    with flat boundaries and :attr:`Graph.edge_space` being a ``Box`` with flat boundaries or
    ``None``. The box has exactly :func:`flatdim` dimensions. Flattening a sample
    of the original space has the same effect as taking a sample of the flattened
    space. However, sampling from the flattened space is not necessarily reversible.
    For example, sampling from a flattened Discrete space is the same as sampling from
    a Box, and the results may not be integers or one-hot encodings. This may result in
    errors or non-uniform sampling.

    Args:
        space: The space to flatten

    Returns:
        A flattened Box

    Raises:
        NotImplementedError: if the space is not defined in :mod:`gymnasium.spaces`.

    Example - Flatten spaces.Box:
        >>> from gymnasium.spaces import Box
        >>> box = Box(0.0, 1.0, shape=(3, 4, 5))
        >>> box
        Box(0.0, 1.0, (3, 4, 5), float32)
        >>> flatten_space(box)
        Box(0.0, 1.0, (60,), float32)
        >>> flatten(box, box.sample()) in flatten_space(box)
        True

    Example - Flatten spaces.Discrete:
        >>> from gymnasium.spaces import Discrete
        >>> discrete = Discrete(5)
        >>> flatten_space(discrete)
        Box(0, 1, (5,), int64)
        >>> flatten(discrete, discrete.sample()) in flatten_space(discrete)
        True

    Example - Flatten spaces.Dict:
        >>> from gymnasium.spaces import Dict, Discrete, Box
        >>> space = Dict({"position": Discrete(2), "velocity": Box(0, 1, shape=(2, 2))})
        >>> flatten_space(space)
        Box(0.0, 1.0, (6,), float64)
        >>> flatten(space, space.sample()) in flatten_space(space)
        True

    Example - Flatten spaces.Graph:
        >>> from gymnasium.spaces import Graph, Discrete, Box
        >>> space = Graph(node_space=Box(low=-100, high=100, shape=(3, 4)), edge_space=Discrete(5))
        >>> flatten_space(space)
        Graph(Box(-100.0, 100.0, (12,), float32), Box(0, 1, (5,), int64))
        >>> flatten(space, space.sample()) in flatten_space(space)
        True
    """
    raise NotImplementedError(f"Unknown space: `{space}`")


def flatten_space(space: Space) -> Union[Dict, Sequence, Tuple, Graph]:
    """Flatten a space into a space that is as flat as possible.

    This function will attempt to flatten `space` into a single :class:`Box` space.
    However, this might not be possible when `space` is an instance of :class:`Graph`,
    :class:`Sequence` or a compound space that contains a :class:`Graph` or :class:`Sequence`space.
    This is equivalent to :func:`flatten`, but operates on the space itself. The
    result for non-graph spaces is always a `Box` with flat boundaries. While
    the result for graph spaces is always a `Graph` with `node_space` being a `Box`
    with flat boundaries and `edge_space` being a `Box` with flat boundaries or
    `None`. The box has exactly :func:`flatdim` dimensions. Flattening a sample
    of the original space has the same effect as taking a sample of the flattenend
    space.

    Example::

        >>> box = Box(0.0, 1.0, shape=(3, 4, 5))
        >>> box
        Box(3, 4, 5)
        >>> flatten_space(box)
        Box(60,)
        >>> flatten(box, box.sample()) in flatten_space(box)
        True

    Example that flattens a discrete space::

        >>> discrete = Discrete(5)
        >>> flatten_space(discrete)
        Box(5,)
        >>> flatten(box, box.sample()) in flatten_space(box)
        True

    Example that recursively flattens a dict::

        >>> space = Dict({"position": Discrete(2), "velocity": Box(0, 1, shape=(2, 2))})
        >>> flatten_space(space)
        Box(6,)
        >>> flatten(space, space.sample()) in flatten_space(space)
        True


    Example that flattens a graph::

        >>> space = Graph(node_space=Box(low=-100, high=100, shape=(3, 4)), edge_space=Discrete(5))
        >>> flatten_space(space)
        Graph(Box(-100.0, 100.0, (12,), float32), Box(0, 1, (5,), int64))
        >>> flatten(space, space.sample()) in flatten_space(space)
        True

    Args:
        space: The space to flatten

    Returns:
        A flattened Box

    Raises:
        NotImplementedError: if the space is not defined in ``gym.spaces``.
    """
    raise NotImplementedError(f"Unknown space: `{space}`")

