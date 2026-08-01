
def rrelu(
    input: Tensor,
    lower: float = 1.0 / 8,
    upper: float = 1.0 / 3,
    training: bool = False,
    inplace: bool = False,
) -> Tensor:  # noqa: D400,D402
    r"""rrelu(input, lower=1./8, upper=1./3, training=False, inplace=False) -> Tensor

    Randomized leaky ReLU.

    See :class:`~torch.nn.RReLU` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            rrelu,
            (input,),
            input,
            lower=lower,
            upper=upper,
            training=training,
            inplace=inplace,
        )
    if inplace:
        result = torch.rrelu_(input, lower, upper, training)
    else:
        result = torch.rrelu(input, lower, upper, training)
    return result


def rrelu(g: jit_utils.GraphContext, input, lower, upper, training, generator):
    if not training:
        slope = (upper + lower) / 2.0
        return g.op("LeakyRelu", input, alpha_f=slope)
    p = g.op("RandomUniformLike", input, high_f=upper, low_f=lower)
    return g.op("PRelu", input, p)

