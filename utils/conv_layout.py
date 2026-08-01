
def conv_layout(
    x: TensorBox,
    weight: TensorBox,
    bias: TensorBox | None,
    stride: Sequence[int],
    padding: tuple[int, ...],
    dilation: tuple[int, ...],
    transposed: bool,
    output_padding: tuple[int, ...],
    groups: int,
) -> ir.Layout:
    """Determine output layout for a convolution"""
    # We use guard_int_seq rather than size_hints because the output shape
    # depends on these values — if they ever contained symbols, size_hints
    # would silently substitute a hint that could be wrong, producing an
    # incorrect layout. guard_int_seq will install a proper guard instead.
    # Note: stride and padding are already guarded via guard_int_seq in
    # convolution() above, but we guard all four here so conv_layout is
    # self-contained and doesn't rely on callers.
    guard = V.graph.sizevars.guard_int_seq
    with V.graph.fake_mode:
        output = torch.ops.aten.convolution(
            ir.ir_node_to_tensor(x),
            ir.ir_node_to_tensor(weight),
            ir.ir_node_to_tensor(bias),
            guard(stride),
            guard(padding),
            guard(dilation),
            transposed,
            guard(output_padding),
            groups,
        )
        sizes = ir.convert_shape_to_inductor(output.size())
        stride = ir.convert_shape_to_inductor(output.stride())  # type: ignore[assignment]

    return ir.FixedLayout(
        x.get_device_or_error(),
        x.get_dtype(),
        sizes,
        stride,
    )

