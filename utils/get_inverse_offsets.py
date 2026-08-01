
def get_inverse_offsets(
    offsets: TensorBox,
    jagged_len: int | sympy.Expr,
    realize: bool = True,
) -> TensorBox:
    """
    Returns "inverse_offsets" - the inverse of the offsets array.
    offsets maps batch index (dense) to jagged index (i.e. offset into jagged tensor).
    inverse_offsets maps jagged index to batch index.

    e.g. for offsets [0, 3, 4, 9, 10] this will return
    inverse_offsets = [0, 0, 0, 1, 2, 2, 2, 2, 2, 3]

    For the given offsets, the computed inverse_offsets are cached
    on the first call and reused in the further calls.
    """

    if hasattr(offsets, "inverse_offsets"):
        # inverse_offsets are already computed
        # for these offsets: can reuse
        return offsets.inverse_offsets

    # ops.bucketize takes offsets.get_name() which doesn't exist on Pointwise
    # kernels, i.e. we need to realize it before using. In other words, we need
    # offsets to be in global memory so that we can binary search over the
    # entire tensor
    offsets.realize()
    device: torch.device = offsets.get_device_or_error()
    dtype: torch.dtype = offsets.get_dtype()

    # pyre-ignore[2,3]
    def inner_fn(index):
        idx = index[0]
        bucket = ops.bucketize(
            values=ops.index_expr(idx, dtype),
            boundaries=(
                offsets.get_name(),
                offsets.get_size()[-1],
                offsets.get_size()[0] * offsets.get_stride()[0],
                offsets.get_stride()[-1],
            ),
            boundary_indices=0,
            indexing_dtype=dtype,
            right=True,
        )
        # ops.bucketize above returns 1-based bucket indices,
        # but we need 0-based, hence we subtract 1 from batch
        return bucket - 1

    inverse_offsets = Pointwise.create(
        device=device,
        dtype=dtype,
        inner_fn=inner_fn,
        ranges=[jagged_len],
    )

    if realize:
        # "freeze" the node so that it doesn't get inlined downstream.
        inverse_offsets.realize()

    # cache inverse_offsets for further reuse
    offsets.inverse_offsets = inverse_offsets  # type: ignore[attr-defined]

    return inverse_offsets

