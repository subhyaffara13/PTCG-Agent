
def pooling_size(x, i, kernel_size, stride, padding, ceil_mode, *, dilation=None):
    if dilation is None:
        dilation = [1] * len(padding)

    x_out = FloorDiv(
        x + 2 * padding[i] - dilation[i] * (kernel_size[i] - 1) + (stride[i] - 1),
        stride[i],
    )

    if ceil_mode:
        x_alt = FloorDiv(
            x
            + 2 * padding[i]
            - dilation[i] * (kernel_size[i] - 1)
            + 2 * (stride[i] - 1),
            stride[i],
        )
        if V.graph.sizevars.guard_or_false(
            sympy.Ge((x_alt - 1) * stride[i] - x - padding[i], 0)
        ):
            # Sliding windows must start within the input or left padding
            x_alt -= 1  # type: ignore[assignment]
        if V.graph.sizevars.guard_or_false(sympy.Eq(x_out, x_alt)):
            # ceil mode is actually a no-op, lets guard on that
            ceil_mode = False
        else:
            x_out = x_alt
    return x_out, ceil_mode

