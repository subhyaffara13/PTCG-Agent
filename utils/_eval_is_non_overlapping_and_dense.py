
def _eval_is_non_overlapping_and_dense(
    sizes: Sequence[int], strides: Sequence[int]
) -> bool:
    """
    Evaluates whether a tensor with the given sizes and strides is non-overlapping and dense.

    A tensor is non-overlapping if there's no memory location that belongs to more than one element.
    A tensor is dense if all elements are stored in memory without gaps.

    Args:
        sizes: Sequence of dimension sizes for the tensor
        strides: Sequence of strides for the tensor

    Returns:
        True if the tensor is non-overlapping and dense, False otherwise
    """
    dim = len(sizes)

    # Short-circuits for tensors of rank one, which are
    # non-overlapping and "dense" if their stride is one
    # or it is a 0/1 element tensor
    if dim == 1:
        return strides[0] == 1 or sizes[0] < 2

    # Checks that there exists a permutation of the strides s.t. the tensor would be contiguous
    # Sorts (length, stride) pairs by stride
    lengths_and_strides = sorted(zip(sizes, strides), key=operator.itemgetter(1))

    # Unlike the C++ code, we don't move the 0/1 size dimensions to the
    # end.  So we have to keep going for this code.
    expected_stride = 1
    for length, stride in lengths_and_strides:
        if length == 1:
            continue

        if stride != expected_stride:
            return False

        expected_stride *= length

    return True

