
def margin_ranking_loss(
    input1: Tensor,
    input2: Tensor,
    target: Tensor,
    margin: float = 0,
    size_average: bool | None = None,
    reduce: bool | None = None,
    reduction: str = "mean",
) -> Tensor:  # noqa: D400,D402
    r"""Compute the margin ranking loss.

    See :class:`~torch.nn.MarginRankingLoss` for details.

    Args:
        input1 (Tensor): Predicted values.
        input2 (Tensor): Predicted values.
        target (Tensor): Ground truth values.
        size_average (bool, optional): Deprecated (see :attr:`reduction`).
        reduce (bool, optional): Deprecated (see :attr:`reduction`).
        reduction (str, optional): Specifies the reduction to apply to the output:
                                   'none' | 'mean' | 'sum'. 'mean': the mean of the output is taken.
                                   'sum': the output will be summed. 'none': no reduction will be applied.
                                   Default: 'mean'.

    Returns:
        Tensor: Margin ranking loss.
    """
    if has_torch_function_variadic(input1, input2, target):
        return handle_torch_function(
            margin_ranking_loss,
            (input1, input2, target),
            input1,
            input2,
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
    if input1.dim() != input2.dim() or input1.dim() != target.dim():
        raise RuntimeError(
            f"margin_ranking_loss : All input tensors should have same dimension but got sizes: "
            f"input1: {input1.size()}, input2: {input2.size()}, target: {target.size()} "
        )
    return torch.margin_ranking_loss(input1, input2, target, margin, reduction_enum)


def margin_ranking_loss(
    input1: TensorLikeType,
    input2: TensorLikeType,
    target: TensorLikeType,
    margin: float = 0.0,
    reduction: str = "mean",
) -> TensorLikeType:
    # loss_without_reduction = max(0, -target * (input1 - input2) + margin)
    if input1.ndim != input2.ndim or input1.ndim != target.ndim:
        raise RuntimeError(
            "margin_ranking_loss : All input tensors should have same dimension but got sizes: "
            f"input1: {input1.shape}, input2: {input2.shape}, target: {target.shape} "
        )
    _check_reduction_value(reduction)
    loss = torch.clamp_min(-target * (input1 - input2) + margin, 0)
    return _apply_loss_reduction(loss, reduction)

