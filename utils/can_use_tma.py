
def can_use_tma(
    *matrices: IRNode, output_layout: Layout | None = None, add_guards: bool = False
) -> bool:
    """
    Return True iff *all* supplied tensors satisfy the CUDA TMA constraints
    that Triton relies on today.
    * https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__TENSOR__MEMORY.html

    A tensor is accepted when:
      * 1 ≤ rank ≤ 5 (cuTensorMapEncodeTiled)
      * dtype in _TMA_SUPPORTED_DTYPES (CUtensorMapDataType enum)
      * Base pointer 16-byte aligned
      * Exactly one contiguous ("inner") dim with stride 1
      * All "outer" dims have 16-byte aligned strides
      * Inner dim size × itemsize is a multiple of 16
      * For 1-byte dtypes (e.g. FP8), inner dim ≥ 32
    """
    from torch.utils._triton import has_triton_tma_device

    from .virtualized import V

    def _aligned(expr_bytes: int | sympy.Expr) -> bool:
        return V.graph.sizevars.statically_known_multiple_of(expr_bytes, TMA_ALIGNMENT)

    def _is_tma_compatible_layout(layout: Layout | None) -> bool:
        if layout is None:
            return True
        sizes = layout.size
        strides = layout.stride
        dtype = layout.dtype

        # Verify the output is 16-byte aligned
        if not _aligned(layout.offset):
            return False

        return _is_tma_compatible(sizes, strides, dtype)

    def _is_tma_compatible_matrix(m: IRNode) -> bool:
        sizes = m.get_size()
        strides = m.get_stride()
        dtype = m.get_dtype()

        # Base pointer 16-byte aligned
        if m.get_name() in V.graph.unaligned_buffers:
            return False

        if (m_device := m.get_device()) is not None and m_device.type == "xpu":
            return _is_tma_compatible_xpu(sizes, strides, dtype)

        return _is_tma_compatible(sizes, strides, dtype)

    def _is_tma_compatible(
        sizes: Sequence[sympy.Expr],
        strides: Sequence[_IntLike],
        dtype: torch.dtype,
    ) -> bool:
        rank = len(sizes)
        itemsize = dtype.itemsize

        if rank < 1 or rank > 5:
            return False

        if dtype not in _TMA_SUPPORTED_DTYPES:
            return False

        if add_guards:
            sizes_i = V.graph.sizevars.guard_int_seq(sizes)
            strides_i = V.graph.sizevars.guard_int_seq(strides)
        else:
            sizes_i = [
                V.graph.sizevars.replace_backed_symbols_with_hints(s) for s in sizes
            ]
            strides_i = [
                V.graph.sizevars.replace_backed_symbols_with_hints(st) for st in strides
            ]

        # Find the single contiguous ("inner") dim
        inner = [
            i
            for i, st in enumerate(strides_i)
            if V.graph.sizevars.statically_known_equals(st, 1)
        ]
        if len(inner) != 1:
            return False
        inner_idx = inner[0]

        # All "outer" dims must have 16-byte aligned strides
        for i, st in enumerate(strides_i):
            if i == inner_idx:
                continue
            if not _aligned(st * itemsize):
                return False

        # Inner dim byte width must be a multiple of 16 B
        inner_dim = sizes_i[inner_idx]
        if not _aligned(inner_dim * itemsize):
            return False

        # 1-byte dtypes (FP8 etc.) need inner dim ≥ 32 for tensor core alignment
        if itemsize == 1 and not V.graph.sizevars.statically_known_geq(inner_dim, 32):
            return False

        return True

    def _is_tma_compatible_xpu(
        sizes: Sequence[sympy.Expr],
        strides: Sequence[_IntLike],
        dtype: torch.dtype,
    ) -> bool:
        # Make sure the last dimension is contiguous
        last_stride = strides[-1]
        last_stride_hint = V.graph.sizevars.replace_backed_symbols_with_hints(
            last_stride
        )
        if not V.graph.sizevars.statically_known_equals(last_stride_hint, 1):
            return False

        # Triton's type of index is uint32, so all dimensions must fit in uint32
        MAX_UINT32 = 2**32 - 1
        for size in sizes:
            size_hint = V.graph.sizevars.replace_backed_symbols_with_hints(size)
            if V.graph.sizevars.statically_known_gt(size_hint, MAX_UINT32):
                return False

        return True

    return (
        has_triton_tma_device()
        and all(_is_tma_compatible_matrix(m) for m in matrices)
        and _is_tma_compatible_layout(output_layout)
    )

