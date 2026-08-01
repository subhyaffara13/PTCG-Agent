
def smooth_l1_loss(
    input: Tensor,
    target: Tensor,
    size_average: bool | None = None,
    reduce: bool | None = None,
    reduction: str = "mean",
    beta: float = 1.0,
) -> Tensor:
    r"""Compute the Smooth L1 loss.

    Function uses a squared term if the absolute
    element-wise error falls below beta and an L1 term otherwise.

    See :class:`~torch.nn.SmoothL1Loss` for details.

    Args:
        input (Tensor): Predicted values.
        target (Tensor): Ground truth values.
        size_average (bool, optional): Deprecated (see :attr:`reduction`).
        reduce (bool, optional): Deprecated (see :attr:`reduction`).
        reduction (str, optional): Specifies the reduction to apply to the output:
                                   'none' | 'mean' | 'sum'. 'mean': the mean of the output is taken.
                                   'sum': the output will be summed. 'none': no reduction will be applied.
                                   Default: 'mean'.
        beta (float, optional): Specifies the threshold at which to change from the squared
            term to the L1 term in the loss calculation. This value must be positive.
            Default: 1.0.

    Returns:
        Tensor: L1 loss (optionally weighted).
    """
    if has_torch_function_variadic(input, target):
        return handle_torch_function(
            smooth_l1_loss,
            (input, target),
            input,
            target,
            size_average=size_average,
            reduce=reduce,
            reduction=reduction,
            beta=beta,
        )
    if target.size() != input.size():
        warnings.warn(
            f"Using a target size ({target.size()}) that is different to the input size ({input.size()}). "
            "This will likely lead to incorrect results due to broadcasting. "
            "Please ensure they have the same size.",
            stacklevel=2,
        )
    if size_average is not None or reduce is not None:
        reduction = _Reduction.legacy_get_string(size_average, reduce)

    expanded_input, expanded_target = torch.broadcast_tensors(input, target)

    if beta == 0.0:
        return torch._C._nn.l1_loss(
            expanded_input,
            expanded_target,
            # pyrefly: ignore [bad-argument-type]
            _Reduction.get_enum(reduction),
        )
    else:
        return torch._C._nn.smooth_l1_loss(
            expanded_input,
            expanded_target,
            # pyrefly: ignore [bad-argument-type]
            _Reduction.get_enum(reduction),
            beta,
        )


def smooth_l1_loss(
    self: Tensor,
    target: Tensor,
    reduction: int = Reduction.MEAN.value,
    beta: float = 1.0,
):
    loss = (self - target).abs()

    loss = torch.where(loss < beta, 0.5 * loss**2 / beta, loss - 0.5 * beta)
    return apply_loss_reduction(loss, reduction)


def smooth_l1_loss(
    input: TensorLikeType,
    target: TensorLikeType,
    size_average: bool | None = None,
    reduce: bool | None = None,
    reduction: str = "mean",
    beta: float = 1.0,
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.smooth_l1_loss
    """
    if size_average is not None or reduce is not None:
        # TODO: Raise exception instead of converting value.  This is only for
        # primTorch since it can drop support for deprecated arguments.
        # msg = "size_average and reduce args are deprecated, please use reduction argument."
        reduction = _get_string_reduction_arg(size_average=size_average, reduce=reduce)
    _check_reduction_value(reduction)

    if beta == 0.0:
        return torch.nn.functional.l1_loss(
            input, target, size_average=size_average, reduce=reduce, reduction=reduction
        )
    else:
        loss = torch.abs(input - target)

        loss = torch.where(loss < beta, 0.5 * loss**2 / beta, loss - 0.5 * beta)
        return _apply_loss_reduction(loss, reduction)

