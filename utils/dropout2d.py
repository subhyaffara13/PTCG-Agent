
def dropout2d(
    input: Tensor,
    p: float = 0.5,
    training: bool = True,
    inplace: bool = False,
) -> Tensor:
    r"""Randomly zero out entire channels (a channel is a 2D feature map).

    For example, the :math:`j`-th channel of the :math:`i`-th sample in the
    batched input is a 2D tensor :math:`\text{input}[i, j]` of the input tensor.
    Each channel will be zeroed out independently on every forward call with
    probability :attr:`p` using samples from a Bernoulli distribution.

    See :class:`~torch.nn.Dropout2d` for details.

    Args:
        p: probability of a channel to be zeroed. Default: 0.5
        training: apply dropout if is ``True``. Default: ``True``
        inplace: If set to ``True``, will do this operation in-place. Default: ``False``
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            dropout2d, (input,), input, p=p, training=training, inplace=inplace
        )
    if p < 0.0 or p > 1.0:
        raise ValueError(f"dropout probability has to be between 0 and 1, but got {p}")
    inp_dim = input.dim()
    if inp_dim not in (3, 4):
        warn_msg = (
            f"dropout2d: Received a {inp_dim}-D input to dropout2d, which is deprecated "
            "and will result in an error in a future release. To retain the behavior "
            "and silence this warning, please use dropout instead. Note that dropout2d "
            "exists to provide channel-wise dropout on inputs with 2 spatial dimensions, "
            "a channel dimension, and an optional batch dimension (i.e. 3D or 4D inputs)."
        )
        warnings.warn(warn_msg, stacklevel=2)

    # TODO: Properly support no-batch-dim inputs. For now, these are NOT supported; passing
    # a 3D input will perform dropout1d behavior instead. This was done historically and the
    # behavior is maintained here for now.
    # See https://github.com/pytorch/pytorch/issues/77081
    if inp_dim == 3:
        warnings.warn(
            "dropout2d: Received a 3D input to dropout2d and assuming that channel-wise "
            "1D dropout behavior is desired - input is interpreted as shape (N, C, L), where C "
            "is the channel dim. This behavior will change in a future release to interpret the "
            "input as one without a batch dimension, i.e. shape (C, H, W). To maintain the 1D "
            "channel-wise dropout behavior, please switch to using dropout1d instead.",
            stacklevel=2,
        )

    result = (
        _VF.feature_dropout_(input, p, training)
        if inplace
        else _VF.feature_dropout(input, p, training)
    )

    return result

