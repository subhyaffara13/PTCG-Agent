
def sympy_is_channels_last_strides_generic(
    sizes: list[sympy.Basic], strides: list[sympy.Basic], dim_order: list[int]
) -> sympy.Basic:
    import sympy

    from torch.utils._sympy.functions import Max

    dim = len(sizes)

    if dim != len(dim_order):
        return sympy.false

    m = sympy.S.Zero
    r = sympy.true

    # special case for trivial C dimension. default to NCHW
    r &= sympy.Ne(strides[1], 0)

    for d in dim_order:
        r &= sympy.Ne(sizes[d], 0) & (strides[d] >= m)
        # Fallback to NCHW as default layout for ambiguous cases
        # This is the flaw of implicit memory_format from strides.
        # N111 tensor with identical strides for size 1 dimension;
        # Two cases could lead us here:
        # a. N111 contiguous Tensor ([N,1,1,1]@[1,1,1,1])
        # b. N11W contiguous Tensor sliced on the W-dimension.
        # ([N,1,1,1]@[W,W,W,W])
        if d == 0:
            r &= sympy.Ne(m, strides[1])
        # This is necessary to:
        # 1. distinguish the memory_format of N1H1;
        #     [H, 1, 1, 1] channels_last stride
        #     [H, H, 1, 1] contiguous stride
        # 2. permutation of 1C1W:
        #     [1, C, 1, H]@[HC, H, H, 1] transpose(1, 3)
        #     [1, H, 1, C]@[HC, 1, H, H] shouldn't be identified as
        #     channels_last
        m = strides[d] * Max(sizes[d], 1)

    return r

