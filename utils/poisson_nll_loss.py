
def poisson_nll_loss(
    input: Tensor,
    target: Tensor,
    log_input: bool = True,
    full: bool = False,
    size_average: bool | None = None,
    eps: float = 1e-8,
    reduce: bool | None = None,
    reduction: str = "mean",
) -> Tensor:
    r"""Compute the Poisson negative log likelihood loss.

    See :class:`~torch.nn.PoissonNLLLoss` for details.

    Args:
        input: Expectation of underlying Poisson distribution.
        target: Random sample :math:`target \sim \text{Poisson}(input)`.
        log_input: If ``True`` the loss is computed as
            :math:`\exp(\text{input}) - \text{target} * \text{input}`, if ``False`` then loss is
            :math:`\text{input} - \text{target} * \log(\text{input}+\text{eps})`. Default: ``True``
        full: Whether to compute full loss, i. e. to add the Stirling
            approximation term. Default: ``False``
            :math:`\text{target} * \log(\text{target}) - \text{target} + 0.5 * \log(2 * \pi * \text{target})`.
        size_average (bool, optional): Deprecated (see :attr:`reduction`).
        eps (float, optional): Small value to avoid evaluation of :math:`\log(0)` when
            :attr:`log_input`\ =\ ``False``. Default: 1e-8
        reduce (bool, optional): Deprecated (see :attr:`reduction`).
        reduction (str, optional): Specifies the reduction to apply to the output:
            ``'none'`` | ``'mean'`` | ``'sum'``. ``'none'``: no reduction will be applied,
            ``'mean'``: the sum of the output will be divided by the number of
            elements in the output, ``'sum'``: the output will be summed. Note: :attr:`size_average`
            and :attr:`reduce` are in the process of being deprecated, and in the meantime,
            specifying either of those two args will override :attr:`reduction`. Default: ``'mean'``

    """
    if has_torch_function_variadic(input, target):
        return handle_torch_function(
            poisson_nll_loss,
            (input, target),
            input,
            target,
            log_input=log_input,
            full=full,
            size_average=size_average,
            eps=eps,
            reduce=reduce,
            reduction=reduction,
        )
    if size_average is not None or reduce is not None:
        reduction = _Reduction.legacy_get_string(size_average, reduce)
    if reduction != "none" and reduction != "mean" and reduction != "sum":
        ret = input
        raise ValueError(reduction + " is not a valid value for reduction")

    ret = torch.poisson_nll_loss(
        input, target, log_input, full, eps, _Reduction.get_enum(reduction)
    )
    return ret


def poisson_nll_loss(
    input: TensorLikeType,
    target: TensorLikeType,
    log_input: bool = True,
    full: bool = False,
    size_average: bool | None = None,
    eps: float = 1e-8,
    reduce: bool | None = None,
    reduction: str = "mean",
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.poisson_nll_loss
    """
    if size_average is not None or reduce is not None:
        # TODO: Raise exception instead of converting value.  This is only for
        # primTorch since it can drop support for deprecated arguments.
        # msg = "size_average and reduce args are deprecated, please use reduction argument."
        reduction = _get_string_reduction_arg(size_average=size_average, reduce=reduce)
    _check_reduction_value(reduction)
    if log_input:
        loss = torch.exp(input) - target * input
    else:
        loss = input - target * torch.log(input + eps)

    if full:
        stirling_term = (
            target * torch.log(target) - target + 0.5 * torch.log(2 * torch.pi * target)
        )
        # avoid inplace add
        loss = loss + stirling_term.masked_fill(target <= 1, 0)
    return _apply_loss_reduction(loss, reduction)

