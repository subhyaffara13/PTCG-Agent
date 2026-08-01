
def multi_margin_loss(
    input: Tensor,
    target: Tensor,
    p: int = 1,
    margin: float = 1.0,
    weight: Tensor | None = None,
    size_average: bool | None = None,
    reduce: bool | None = None,
    reduction: str = "mean",
) -> Tensor:  # noqa: D400,D402
    r"""Compute the multi margin loss, with optional weighting.

    See :class:`~torch.nn.MultiMarginLoss` for details.

    Args:
        input (Tensor): Predicted values.
        target (Tensor): Ground truth values.
        p (int, optional): Has a default value of 1. 1 and 2 are the only supported values.
        margin (float, optional): Margin for multi margin loss. Has a default value of 1.
        weight (Tensor, optional): Weights for each sample. Default: None.
        size_average (bool, optional): Deprecated (see :attr:`reduction`).
        reduce (bool, optional): Deprecated (see :attr:`reduction`).
        reduction (str, optional): Specifies the reduction to apply to the output:
                                  'none' | 'mean' | 'sum'. 'mean': the mean of the output is taken.
                                  'sum': the output will be summed. 'none': no reduction will be applied.
                                  Default: 'mean'.

    Returns:
        Tensor: Multi margin loss (optionally weighted).
    """
    if has_torch_function_variadic(input, target, weight):
        return handle_torch_function(
            multi_margin_loss,
            (input, target, weight),
            input,
            target,
            p=p,
            margin=margin,
            weight=weight,
            size_average=size_average,
            reduce=reduce,
            reduction=reduction,
        )
    if size_average is not None or reduce is not None:
        reduction_enum = _Reduction.legacy_get_enum(size_average, reduce)
    else:
        reduction_enum = _Reduction.get_enum(reduction)
    if p != 1 and p != 2:
        raise ValueError("only p == 1 and p == 2 supported")
    if weight is not None:
        if weight.dim() != 1:
            raise ValueError("weight must be one-dimensional")

    return torch._C._nn.multi_margin_loss(
        input,
        target,
        p,
        margin,
        weight,
        # pyrefly: ignore [bad-argument-type]
        reduction_enum,
    )


def multi_margin_loss(
    input: Tensor,
    target: Tensor,
    p: NumberType = 1,
    margin: NumberType = 1,
    weight: Tensor | None = None,
    reduction: int = Reduction.MEAN.value,
) -> Tensor:
    input = torch.atleast_2d(input)
    target = torch.atleast_1d(target)
    nframe = input.shape[0]
    dim = input.shape[1]
    torch._check(p == 1 or p == 2, lambda: "only p == 1 and p == 2 supported")
    torch._check(
        input.ndim == 2 and dim != 0,
        lambda: f"Expected non-empty vector or matrix with optional 0-dim batch size, but got: {input.shape}",
    )
    torch._check(
        target.ndim == 1 and target.numel() == nframe,
        lambda: f"inconsistent target size, expected {nframe} but got {target.shape}",
    )
    if weight is not None:
        weight = torch.atleast_1d(weight)
        torch._check(
            weight.ndim == 1 and weight.numel() == dim,  # type: ignore[union-attr]
            lambda: f"inconsistent weight size, expected {dim} but got {weight.shape}",  # type: ignore[union-attr]
        )
    target = target.unsqueeze(1)
    u = torch.gather(input, dim=1, index=target)
    z = margin - u + input
    z = z.clamp_min(0)
    z = z if p == 1 else z * z
    if weight is not None:
        z = z * weight[target]
    idx = torch.arange(dim, device=input.device)
    z = torch.where(idx != target, z, 0)
    if reduction == Reduction.MEAN.value:
        return z.mean()
    elif reduction == Reduction.SUM.value:
        return z.sum() / z.shape[1]
    else:
        return z.mean(dim=1)

