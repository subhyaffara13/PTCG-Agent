
def cosine_embedding_loss(
    input1: Tensor,
    input2: Tensor,
    target: Tensor,
    margin: float = 0,
    size_average: bool | None = None,
    reduce: bool | None = None,
    reduction: str = "mean",
) -> Tensor:  # noqa: D400,D402
    r"""Compute the cosine embedding loss.

    See :class:`~torch.nn.CosineEmbeddingLoss` for details.

    Args:
       input1 (Tensor): Predicted values.
       input2 (Tensor): Predicted values.
       target (Tensor): Ground truth values.
       margin (float, optional): Margin for cosine embedding. Has a default value of 0.
       size_average (bool, optional): Deprecated (see :attr:`reduction`).
       reduce (bool, optional): Deprecated (see :attr:`reduction`).
       reduction (str, optional): Specifies the reduction to apply to the output:
                                  'none' | 'mean' | 'sum'. 'mean': the mean of the output is taken.
                                  'sum': the output will be summed. 'none': no reduction will be applied.
                                  Default: 'mean'.

    Returns:
       Tensor: Cosine embedding loss.
    """
    if has_torch_function_variadic(input1, input2, target):
        return handle_torch_function(
            cosine_embedding_loss,
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
    return torch.cosine_embedding_loss(input1, input2, target, margin, reduction_enum)

