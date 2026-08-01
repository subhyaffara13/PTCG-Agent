
def multilabel_margin_loss(
    input: Tensor,
    target: Tensor,
    size_average: bool | None = None,
    reduce: bool | None = None,
    reduction: str = "mean",
) -> Tensor:  # noqa: D400,D402
    r"""Compute the multilabel margin loss.

    See :class:`~torch.nn.MultiLabelMarginLoss` for details.

    Args:
       input (Tensor): Predicted values.
       target (Tensor): Ground truth values.
       size_average (bool, optional): Deprecated (see :attr:`reduction`).
       reduce (bool, optional): Deprecated (see :attr:`reduction`).
       reduction (str, optional): Specifies the reduction to apply to the output:
                                  'none' | 'mean' | 'sum'. 'mean': the mean of the output is taken.
                                  'sum': the output will be summed. 'none': no reduction will be applied.
                                  Default: 'mean'.

    Returns:
       Tensor: Mutilabel margin loss.
    """
    if has_torch_function_variadic(input, target):
        return handle_torch_function(
            multilabel_margin_loss,
            (input, target),
            input,
            target,
            size_average=size_average,
            reduce=reduce,
            reduction=reduction,
        )
    if size_average is not None or reduce is not None:
        reduction_enum = _Reduction.legacy_get_enum(size_average, reduce)
    else:
        reduction_enum = _Reduction.get_enum(reduction)
    # pyrefly: ignore [bad-argument-type]
    return torch._C._nn.multilabel_margin_loss(input, target, reduction_enum)

