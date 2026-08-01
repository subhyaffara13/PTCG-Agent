
def _bitonic_merge_with_index(
    x,
    idxs,
    rnumel,
    stage: tl.constexpr,
    alternating: tl.constexpr,
    n_dims: tl.constexpr,
    stable: tl.constexpr,
    descending: tl.constexpr,
):
    n_outer: tl.constexpr = x.numel >> n_dims
    tl.static_assert(stage <= n_dims)
    # flip denotes whether to re-arrange sub-sequences of elements in ascending or
    # descending order.
    # if flip = 00000000... then all elements will be re-arranged ascendingly at this stage
    # if flip = 00110011... then all the elements will be re-arranged alternatingly (with
    # a stride of 2) at this stage
    if alternating:
        shape: tl.constexpr = [n_outer * 2 ** (n_dims - 1 - stage), 2, 2**stage]
        flip = tl.reshape(
            tl.broadcast_to(tl.arange(0, 2)[None, :, None], shape), x.shape
        )
    else:
        flip = False
    # perform `stage` rounds of `compare-and-swap`
    for i in tl.static_range(stage):
        x, idxs = _compare_and_swap_with_index(
            x, idxs, rnumel, flip, i + (n_dims - stage), n_dims, stable, descending
        )
    return x, idxs

