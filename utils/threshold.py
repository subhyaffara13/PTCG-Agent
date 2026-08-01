
def threshold(
    a: TensorLikeType,
    threshold: NumberType,
    value: bool | int | float,
    inplace: bool = False,
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.threshold
    """

    if inplace:
        raise NotImplementedError

    return torch.where(a <= threshold, value, a)


def threshold(g: jit_utils.GraphContext, self, threshold, value):
    # See Note [Export inplace]
    if symbolic_helper._scalar(threshold) != 0:
        return symbolic_helper._unimplemented("threshold", "non-zero threshold", self)
    if symbolic_helper._scalar(value) != 0:
        return symbolic_helper._unimplemented("threshold", "non-zero value", self)
    return g.op("Relu", self)


def threshold(input: Tensor, threshold: float, value: float) -> Tensor:
    r"""Applies the quantized version of the threshold function element-wise:

    .. math::
        x = \begin{cases}
                x & \text{if~} x > \text{threshold} \\
                \text{value} & \text{otherwise}
            \end{cases}

    See :class:`~torch.nn.Threshold` for more details.
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.threshold' must be quantized!")
    if threshold is None:
        raise ValueError("Input to 'threshold' must be specified!")
    if value is None:
        raise ValueError("Input to 'value' must be specified!")
    return torch._ops.ops.quantized.threshold(input, threshold, value)


def threshold(
    return_surf,
    surf,
    color,
    threshold=(0, 0, 0),
    diff_color=(0, 0, 0),
    change_return=True,
):
    """given the color it makes return_surf only have areas with the given colour."""

    width, height = surf.get_width(), surf.get_height()

    if change_return:
        return_surf.fill(diff_color)

    try:
        r, g, b = color
    except ValueError:
        r, g, b, a = color

    try:
        tr, tg, tb = color
    except ValueError:
        tr, tg, tb, ta = color

    similar = 0
    for y in range(height):
        for x in range(width):
            c1 = surf.get_at((x, y))

            if (abs(c1[0] - r) < tr) & (abs(c1[1] - g) < tg) & (abs(c1[2] - b) < tb):
                # this pixel is within the threshold.
                if change_return:
                    return_surf.set_at((x, y), c1)
                similar += 1
            # else:
            #    print(c1, c2)

    return similar

