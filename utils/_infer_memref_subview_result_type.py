
def _infer_memref_subview_result_type(
    source_memref_type, offsets, static_sizes, static_strides
):
    source_strides, source_offset = source_memref_type.get_strides_and_offset()
    # "canonicalize" from tuple|list -> list
    offsets, static_sizes, static_strides, source_strides = map(
        list, (offsets, static_sizes, static_strides, source_strides)
    )

    if not all(
        all(_is_static_int_like(i) for i in s)
        for s in [
            static_sizes,
            static_strides,
            source_strides,
        ]
    ):
        raise ValueError(
            "Only inferring from python or mlir integer constant is supported."
        )

    for s in [offsets, static_sizes, static_strides]:
        for idx, i in enumerate(s):
            if _is_constant_int_like(i):
                s[idx] = i.owner.opview.literal_value

    if any(not _is_static_int_like(i) for i in offsets + [source_offset]):
        target_offset = ShapedType.get_dynamic_size()
    else:
        target_offset = source_offset
        for offset, target_stride in zip(offsets, source_strides):
            target_offset += offset * target_stride

    target_strides = []
    for source_stride, static_stride in zip(source_strides, static_strides):
        target_strides.append(source_stride * static_stride)

    # If default striding then no need to complicate things for downstream ops (e.g., expand_shape).
    default_strides = list(accumulate(static_sizes[1:][::-1], operator.mul))[::-1] + [1]
    if target_strides == default_strides and target_offset == 0:
        layout = None
    else:
        layout = StridedLayoutAttr.get(target_offset, target_strides)
    return (
        offsets,
        static_sizes,
        static_strides,
        MemRefType.get(
            static_sizes,
            source_memref_type.element_type,
            layout,
            source_memref_type.memory_space,
        ),
    )

