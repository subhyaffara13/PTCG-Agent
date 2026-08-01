
def tanhshrink(input):  # noqa: D400,D402
    r"""tanhshrink(input) -> Tensor

    Applies element-wise, :math:`\text{Tanhshrink}(x) = x - \text{Tanh}(x)`

    See :class:`~torch.nn.Tanhshrink` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(tanhshrink, (input,), input)
    return input - input.tanh()


def tanhshrink(a: TensorLikeType) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.tanhshrink
    """
    if not isinstance(a, TensorLike):
        raise RuntimeError(
            "Expected a tensor input for an elementwise unary operation!"
        )
    return a - torch.tanh(a)


def tanhshrink(g: jit_utils.GraphContext, self):
    return g.op("Sub", self, tanh(g, self))

