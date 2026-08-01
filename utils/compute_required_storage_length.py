
def compute_required_storage_length(
    shape: ShapeType, strides: StrideType, storage_offset: int
) -> int:
    """Computes the minimum storage size to hold the given tensor geometry.

    Example
    =======

    This is the size of a newly allocated tensor's storage, in units of elements

    >>> t = torch.empty((10, 20))
    >>> compute_required_storage_length(t.shape, t.stride(), t.storage_offset())
    200

    >>> # xdoctest: +SKIP(failing)
    >>> t2 = torch.empty_strided((1, 2, 3), (5, 7, 11))
    >>> size = compute_required_storage_length(
    ...     t2.shape, t2.stride(), t2.storage_offset()
    ... )
    >>> size == t.storage().size()
    True

    A valid tensor may have a larger storage size, but never smaller

    >>> slice = torch.empty(100)[20:40]
    >>> slice.storage().size()
    100

    >>> compute_required_storage_length(
    ...     slice.shape, slice.stride(), slice.storage_offset()
    ... )
    40

    """
    from torch.fx.experimental.symbolic_shapes import guard_or_false

    # Short-circuits if the shape has no elements
    # Note: we are unsafely assuming tensor is not empty here, without
    # runtime assertions.
    if guard_or_false(reduce(operator.mul, shape, 1) == 0):
        return 0

    max_offset = sum((x - 1) * y for x, y in zip(shape, strides))
    # +1 to account for the first element which offsets are taken from
    return 1 + storage_offset + max_offset

