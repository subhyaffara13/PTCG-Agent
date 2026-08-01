
def compute_local_stride(
    global_stride: ShapeType, local_shape: ShapeType
) -> tuple[int, ...]:
    """
    Compute the stride of a local tensor shard, given the global stride and local shape.

    Derives strides by preserving the memory layout (dimension ordering) implied
    by the global strides, then computing contiguous strides for the local shape
    in that order.  Assumes the global tensor is non-overlapping and dense.
    """
    ndim = len(global_stride)
    # Sort dims by global stride descending to recover memory layout order.
    # Stable sort preserves original dim order for ties, which only occur
    # on size-1 dims where the stride value is semantically irrelevant.
    perm = sorted(range(ndim), key=lambda d: global_stride[d], reverse=True)
    local_strides = [0] * ndim
    s = 1
    for d in reversed(perm):
        local_strides[d] = s
        s *= local_shape[d]
    return tuple(local_strides)

