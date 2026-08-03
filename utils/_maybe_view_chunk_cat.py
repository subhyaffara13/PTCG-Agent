import math


def _maybe_view_chunk_cat(
    res: "torch.Tensor", group_size: int, gather_dim: int
) -> "torch.Tensor":
    """
    This is intuitively the same as torch.cat(torch.chunk(res, group_size,
    dim=0), dim=gather_dim), but returns a view if data movement is not
    necessary.  This operation arises in NCCL all_gather, where you always get
    a result which is concatenated on dim=0, even though actually you may need
    to undo this concatenation and then re-cat on the gather dim.

    When is data-movement not necessary?  Intuitively, we need to understand if
    the unflatten in this reference implementation of this code triggers a
    copy or not:

        chunks = torch.unflatten(res, 0, [group_size, -1])
        return torch.flatten(torch.movedim(chunks, 0, gather_dim), gather_dim, gather_dim + 1)

    Assume res is contiguous (it will be coming out of the collective).  We
    essentially need to know if the movedim maintains the contiguity of the
    tensor.  Moving a dimension typically does NOT preserve contiguity, unless
    EVERY dimension it is moved across is size 1.

    Example: shape [4, d1, d2] with group_size=4, gather_dim=1 -> [1, 4*d1, d2]

        [4, d1, d2] -> [4, 1, d1, d2] -> [1, 4, d1, d2] (contiguous!)

    Example: shape [4, 2, d2] with group_size=4, gather_dim=2 -> [1, 2, 4*d2]

        [4, 2, d2] -> [4, 1, 2, d2] -> [1, 2, 4, d2] (not contiguous!)

    Args:
        res: Tensor with gathered data in dim 0, shape [group_size, ...]
        group_size: Number of ranks in the group
        gather_dim: Dimension to gather along in the output

    Returns:
        Tensor with data rearranged to gather along gather_dim
    """

    if gather_dim == 0:
        # When gather_dim is 0, chunk+cat is a no-op
        return res

    shape = list(res.shape)

    # Optimization: Can use view instead of split+cat when:
    # 1. res.shape[0] == group_size (invariant after all_gather)
    # 2. All dims between 0 and gather_dim (exclusive) have size 1
    from torch.fx.experimental.symbolic_shapes import guard_or_false

    numel_between = math.prod(shape[1:gather_dim]) if gather_dim > 1 else 1

    if guard_or_false(shape[0] == group_size) and guard_or_false(numel_between == 1):
        # View optimization: reshape to collapse dim 0 into gather_dim
        final_shape = (
            [1]  # Dim 0 becomes 1
            + shape[1:gather_dim]  # Dims 1 to gather_dim-1 unchanged
            + [shape[0] * shape[gather_dim]]  # gather_dim gets multiplied by group_size
            + shape[gather_dim + 1 :]  # Rest unchanged
        )
        return res.view(final_shape)
    else:
        # General case: fall back to split + cat
        # This is better than torch.flatten as cat can be vectorized, whereas
        # the contiguous kernel is always bad.
        return _chunk_or_narrow_cat(res, group_size, narrow_dim=0, cat_dim=gather_dim)

