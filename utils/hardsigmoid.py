
def hardsigmoid(input: Tensor, inplace: bool = False) -> Tensor:
    r"""Apply the Hardsigmoid function element-wise.

    .. math::
        \text{Hardsigmoid}(x) = \begin{cases}
            0 & \text{if~} x \le -3, \\
            1 & \text{if~} x \ge +3, \\
            x / 6 + 1 / 2 & \text{otherwise}
        \end{cases}

    Args:
        inplace: If set to ``True``, will do this operation in-place. Default: ``False``

    See :class:`~torch.nn.Hardsigmoid` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(hardsigmoid, (input,), input, inplace=inplace)
    if inplace:
        return torch._C._nn.hardsigmoid_(input)
    return torch._C._nn.hardsigmoid(input)


def hardsigmoid(self: Tensor) -> Tensor:
    return torch.clamp(torch.clamp(self + 3, min=0), max=6) / 6


def hardsigmoid(g: jit_utils.GraphContext, self):
    # Set alpha_f to 1 / 6 to make op equivalent to PyTorch's definition of Hardsigmoid.
    # See https://pytorch.org/docs/stable/generated/torch.nn.Hardsigmoid.html
    return g.op("HardSigmoid", self, alpha_f=1 / 6)


def hardsigmoid(input: Tensor, inplace: bool = False) -> Tensor:
    r"""This is the quantized version of :func:`~torch.nn.functional.hardsigmoid`."""
    if not input.is_quantized:
        raise ValueError("Input to 'quantized.hardsigmoid' must be quantized!")
    if inplace:
        return torch._C._nn.hardsigmoid_(input)  # type: ignore[attr-defined]
    return torch._C._nn.hardsigmoid(input)

