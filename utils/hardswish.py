
def hardswish(input: Tensor, inplace: bool = False) -> Tensor:
    r"""Apply hardswish function, element-wise.

    Follows implementation as described in the paper:
    `Searching for MobileNetV3`_.

    .. math::
        \text{Hardswish}(x) = \begin{cases}
            0 & \text{if~} x \le -3, \\
            x & \text{if~} x \ge +3, \\
            x \cdot (x + 3) /6 & \text{otherwise}
        \end{cases}

    See :class:`~torch.nn.Hardswish` for more details.

    .. _`Searching for MobileNetV3`:
        https://arxiv.org/abs/1905.02244
    """
    if has_torch_function_unary(input):
        return handle_torch_function(hardswish, (input,), input, inplace=inplace)
    if inplace:
        return torch._C._nn.hardswish_(input)
    return torch._C._nn.hardswish(input)


def hardswish(self: Tensor) -> Tensor:
    return self * torch.clamp(torch.clamp(self + 3, min=0), max=6) / 6


def hardswish(g: jit_utils.GraphContext, self):
    return g.op("HardSwish", self)


def hardswish(g: jit_utils.GraphContext, self):
    hs = hardsigmoid(g, self)
    return g.op("Mul", self, hs)


def hardswish(input: Tensor, scale: float, zero_point: int) -> Tensor:
    r"""This is the quantized version of :func:`~torch.nn.functional.hardswish`.

    Args:
        input: quantized input
        scale: quantization scale of the output tensor
        zero_point: quantization zero point of the output tensor
    """
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.hardswish' must be quantized!")
    return torch._ops.ops.quantized.hardswish(input, scale, zero_point)

