
def is_non_overlapping_and_dense_or_false(a: Tensor) -> bool:
    """
    True when a tensor is non-overlapping and dense.

    A tensor is non-overlapping and dense when there exists a permutation of
    its dimensions that is contiguous.
    """
    from torch.fx.experimental.symbolic_shapes import guard_or_false

    if a.is_sparse:
        return False

    return _is_non_overlapping_and_dense_or_false(a.shape, a.stride())

