
def feature_alpha_dropout(
    input: Tensor,
    p: float = 0.5,
    training: bool = False,
    inplace: bool = False,
) -> Tensor:
    r"""Randomly masks out entire channels (a channel is a feature map).

    For example, the :math:`j`-th channel of the :math:`i`-th sample in the batch input
    is a tensor :math:`\text{input}[i, j]` of the input tensor. Instead of
    setting activations to zero, as in regular Dropout, the activations are set
    to the negative saturation value of the SELU activation function.

    Each element will be masked independently on every forward call with
    probability :attr:`p` using samples from a Bernoulli distribution.
    The elements to be masked are randomized on every forward call, and scaled
    and shifted to maintain zero mean and unit variance.

    See :class:`~torch.nn.FeatureAlphaDropout` for details.

    Args:
        p: dropout probability of a channel to be zeroed. Default: 0.5
        training: apply dropout if is ``True``. Default: ``True``
        inplace: If set to ``True``, will do this operation in-place. Default: ``False``
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            feature_alpha_dropout,
            (input,),
            input,
            p=p,
            training=training,
            inplace=inplace,
        )
    if p < 0.0 or p > 1.0:
        raise ValueError(f"dropout probability has to be between 0 and 1, but got {p}")
    return (
        _VF.feature_alpha_dropout_(input, p, training)
        if inplace
        else _VF.feature_alpha_dropout(input, p, training)
    )

