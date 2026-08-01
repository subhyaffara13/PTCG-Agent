
def batch_differing_spaces(spaces: typing.Sequence[Space]) -> Space:
    """Batch a Sequence of spaces where subspaces to contain minor differences.

    Args:
        spaces: A sequence of Spaces with minor differences (the same space type but different parameters).

    Returns:
        A batched space

    Example:
        >>> from gymnasium.spaces import Discrete
        >>> spaces = [Discrete(3), Discrete(5), Discrete(4), Discrete(8)]
        >>> batch_differing_spaces(spaces)
        MultiDiscrete([3 5 4 8])
    """
    assert len(spaces) > 0, "Expects a non-empty list of spaces"
    assert all(
        isinstance(space, type(spaces[0])) for space in spaces
    ), f"Expects all spaces to be the same shape, actual types: {[type(space) for space in spaces]}"
    assert (
        type(spaces[0]) in batch_differing_spaces.registry
    ), f"Requires the Space type to have a registered `batch_differing_space`, current list: {batch_differing_spaces.registry}"

    return batch_differing_spaces.dispatch(type(spaces[0]))(spaces)

