
def _convert_space(space: gym.Space) -> gymnasium.Space:
    """Converts a gym space to a gymnasium space.

    Args:
        space: the space to convert

    Returns:
        The converted space
    """
    if isinstance(space, gym.spaces.Discrete):
        return Discrete(n=space.n)
    elif isinstance(space, gym.spaces.Box):
        return Box(low=space.low, high=space.high, shape=space.shape, dtype=space.dtype)
    elif isinstance(space, gym.spaces.MultiDiscrete):
        return MultiDiscrete(nvec=space.nvec)
    elif isinstance(space, gym.spaces.MultiBinary):
        return MultiBinary(n=space.n)
    elif isinstance(space, gym.spaces.Tuple):
        return Tuple(spaces=tuple(map(_convert_space, space.spaces)))
    elif isinstance(space, gym.spaces.Dict):
        return Dict(spaces={k: _convert_space(v) for k, v in space.spaces.items()})
    elif isinstance(space, gym.spaces.Sequence):
        return Sequence(space=_convert_space(space.feature_space))
    elif isinstance(space, gym.spaces.Graph):
        return Graph(
            node_space=_convert_space(space.node_space),  # type: ignore
            edge_space=_convert_space(space.edge_space),  # type: ignore
        )
    elif isinstance(space, gym.spaces.Text):
        return Text(
            max_length=space.max_length,
            min_length=space.min_length,
            charset=space._char_str,
        )
    else:
        raise NotImplementedError(
            f"Cannot convert space of type {space}. Please upgrade your code to gymnasium."
        )

