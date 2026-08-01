
def alpha_dropout(
    input: Tensor,
    p: float = 0.5,
    training: bool = False,
    inplace: bool = False,
) -> Tensor:
    r"""Apply alpha dropout to the input.

    See :class:`~torch.nn.AlphaDropout` for details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            alpha_dropout, (input,), input, p=p, training=training, inplace=inplace
        )
    if p < 0.0 or p > 1.0:
        raise ValueError(f"dropout probability has to be between 0 and 1, but got {p}")
    return (
        _VF.alpha_dropout_(input, p, training)
        if inplace
        else _VF.alpha_dropout(input, p, training)
    )


def alpha_dropout(
    self: TensorLikeType, p: float = 0.5, training: bool = False, inplace: bool = False
) -> TensorLikeType:
    if inplace:
        raise NotImplementedError

    if not training:
        return self

    torch._check(
        p <= 1 and p >= 0,
        lambda: f"dropout probability has to be between 0 and 1, but got, {p}",
    )

    if p == 1:
        return torch.zeros_like(self)

    if p == 0:
        return self

    dropout_mask = _dropout_helper(self, 1 - p)

    # From paper: Self-Normalizing Neural Networks (https://arxiv.org/pdf/1706.02515.pdf)
    # alpha = - SELU.alpha * SELU.scale, here
    # SELU.alpha = 1.6732632423543772848170429916717 and
    # SELU.scale = 1.0507009873554804934193349852946
    alpha = -1.7580993408473766

    a = 1.0 / math.sqrt((alpha * alpha * p + 1) * (1 - p))
    b = torch.logical_not(dropout_mask)
    b = b * (alpha * a) + alpha * a * p
    dropout_mask = a * dropout_mask

    return self * dropout_mask + b

