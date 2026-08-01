
def softsign(input):  # noqa: D400,D402
    r"""softsign(input) -> Tensor

    Applies element-wise, the function :math:`\text{SoftSign}(x) = \frac{x}{1 + |x|}`

    See :class:`~torch.nn.Softsign` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(softsign, (input,), input)
    return input / (input.abs() + 1)

