
def hinge_embedding_loss(
    input: Tensor,
    target: Tensor,
    margin: float = 1.0,
    size_average: bool | None = None,
    reduce: bool | None = None,
    reduction: str = "mean",
) -> Tensor:  # noqa: D400,D402
    r"""Compute the hinge embedding loss.

    See :class:`~torch.nn.HingeEmbeddingLoss` for details.

    Args:
       input (Tensor): Predicted values.
       target (Tensor): Ground truth values.
       margin (float, optional): Margin for hinge loss. Has a default value of 1.
       size_average (bool, optional): Deprecated (see :attr:`reduction`).
       reduce (bool, optional): Deprecated (see :attr:`reduction`).
       reduction (str, optional): Specifies the reduction to apply to the output:
                                  'none' | 'mean' | 'sum'. 'mean': the mean of the output is taken.
                                  'sum': the output will be summed. 'none': no reduction will be applied.
                                  Default: 'mean'.

    Returns:
       Tensor: Hinge embedding loss.
    """
    if has_torch_function_variadic(input, target):
        return handle_torch_function(
            hinge_embedding_loss,
            (input, target),
            input,
            target,
            margin=margin,
            size_average=size_average,
            reduce=reduce,
            reduction=reduction,
        )
    if size_average is not None or reduce is not None:
        reduction_enum = _Reduction.legacy_get_enum(size_average, reduce)
    else:
        reduction_enum = _Reduction.get_enum(reduction)
    return torch.hinge_embedding_loss(input, target, margin, reduction_enum)


def hinge_embedding_loss(
    input: TensorLikeType,
    target: TensorLikeType,
    margin: float = 1.0,
    reduction: str = "mean",
) -> TensorLikeType:
    # loss_without_reduction = input if y == 1
    #                        = max(0, margin - input) if y == -1
    _check_reduction_value(reduction)
    margin_clamp = torch.clamp_min(margin - input, 0)
    output_margin = torch.where(target != 1, margin_clamp, 0)
    output_self = torch.where(target != -1, input, 0)
    loss = output_margin + output_self
    return _apply_loss_reduction(loss, reduction)

