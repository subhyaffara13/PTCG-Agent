
def nll_loss(
    input: Tensor,
    target: Tensor,
    weight: Tensor | None = None,
    size_average: bool | None = None,
    ignore_index: int = -100,
    reduce: bool | None = None,
    reduction: str = "mean",
) -> Tensor:
    r"""Compute the negative log likelihood loss.

    See :class:`~torch.nn.NLLLoss` for details.

    Args:
        input: :math:`(N, C)` where `C = number of classes` or :math:`(N, C, H, W)`
            in case of 2D Loss, or :math:`(N, C, d_1, d_2, ..., d_K)` where :math:`K \geq 1`
            in the case of K-dimensional loss. `input` is expected to be log-probabilities.
        target: :math:`(N)` where each value is :math:`0 \leq \text{targets}[i] \leq C-1`,
            or :math:`(N, d_1, d_2, ..., d_K)` where :math:`K \geq 1` for
            K-dimensional loss.
        weight (Tensor, optional): A manual rescaling weight given to each
            class. If given, has to be a Tensor of size `C`
        size_average (bool, optional): Deprecated (see :attr:`reduction`).
        ignore_index (int, optional): Specifies a target value that is ignored
            and does not contribute to the input gradient. When :attr:`size_average` is
            ``True``, the loss is averaged over non-ignored targets. Default: -100
        reduce (bool, optional): Deprecated (see :attr:`reduction`).
        reduction (str, optional): Specifies the reduction to apply to the output:
            ``'none'`` | ``'mean'`` | ``'sum'``. ``'none'``: no reduction will be applied,
            ``'mean'``: the sum of the output will be divided by the number of
            elements in the output, ``'sum'``: the output will be summed. Note: :attr:`size_average`
            and :attr:`reduce` are in the process of being deprecated, and in the meantime,
            specifying either of those two args will override :attr:`reduction`. Default: ``'mean'``

    Example::

        >>> # input is of size N x C = 3 x 5
        >>> input = torch.randn(3, 5, requires_grad=True)
        >>> # each element in target has to have 0 <= value < C
        >>> target = torch.tensor([1, 0, 4])
        >>> output = F.nll_loss(F.log_softmax(input, dim=1), target)
        >>> output.backward()
    """
    if has_torch_function_variadic(input, target, weight):
        return handle_torch_function(
            nll_loss,
            (input, target, weight),
            input,
            target,
            weight=weight,
            size_average=size_average,
            ignore_index=ignore_index,
            reduce=reduce,
            reduction=reduction,
        )
    if size_average is not None or reduce is not None:
        reduction = _Reduction.legacy_get_string(size_average, reduce)
    return torch._C._nn.nll_loss_nd(
        input,
        target,
        weight,
        # pyrefly: ignore [bad-argument-type]
        _Reduction.get_enum(reduction),
        ignore_index,
    )


def nll_loss(
    input: TensorLikeType,
    target: TensorLikeType,
    weight: TensorLikeType | None = None,
    size_average: bool | None = None,
    ignore_index: int = -100,
    reduce: bool | None = None,
    reduction: str = "mean",
) -> TensorLikeType:
    """
    Reference implementation of torch.nn.functional.nll_loss
    """
    torch._check(
        input.ndim > 0,
        lambda: f"Expected input tensor to have 1 or more dimensions (got {input.ndim})",
    )

    # TODO: raise exception instead of converting value
    # msg = "size_average and reduce args are deprecated, please use reduction argument."
    # Convert these options for consistency with the eager mode
    if size_average is not None or reduce is not None:
        reduction = _get_string_reduction_arg(size_average=size_average, reduce=reduce)

    # The expected behavior when the target and input have zero elements:
    #   reduction = 'none' --- tensor([])
    #   reduction = 'sum'  --- tensor(0.)
    #   reduction = 'mean' --- tensor(nan)
    # Mean reduction on empty tensors produces NaN. See the discussion in
    # https://github.com/pytorch/pytorch/pull/64572#issuecomment-926504162
    if input.numel() == 0 and target.numel() == 0:
        if reduction == "none":
            return torch.zeros_like(target)
        elif reduction == "sum":
            return torch.empty_like(target)
        else:
            return torch.full_like(target, float("nan"))

    # The _nll_loss_nd helper function handles the most common cases.
    # ndim == 1 (Single Example)
    #   => Batch Size: 1, Input: (C), Target: ()
    # ndim == 2 (k = 1)
    #   => Batch Size: N, Input: (N, C), Target: (N)
    # ndim == 3 (k > 1)
    #   => Batch Size: N, Input: (N, C, K), Target: (N, K)
    if input.ndim <= 3:
        return _nll_loss_nd(input, target, weight, reduction, ignore_index)

    # For ndim > 3, we reshape the input and target to 3-D case.
    # Input (N batch-size, C classes, k-dimensions)
    # Target (N batch-size, k-dimensions)
    torch._check(
        input.ndim > 0 and target.ndim > 0 and target.shape[1:] == input.shape[2:],
        lambda: (
            "Expected input and target to both have ndim > 0 and "
            "target.shape[1:] == input.shape[2:], but got "
            f"target.shape {target.shape} and input.shape {input.shape}"
        ),
    )

    batch_size = input.shape[0]
    num_classes = input.shape[1]
    out_size = [batch_size] + list(target.shape[1:])

    input = torch.reshape(input, [batch_size, num_classes, -1])
    target = torch.reshape(target, [batch_size, -1])
    if reduction != "none":
        return _nll_loss_nd(input, target, weight, reduction, ignore_index)
    else:
        result = _nll_loss_nd(input, target, weight, reduction, ignore_index)
        # reshape flattened inner-dim to original k-dimensions
        return torch.reshape(result, out_size)


def nll_loss(g: jit_utils.GraphContext, self, target, weight, reduction, ignore_index):
    # none reduction : onnx::Constant[value={0}]
    # mean reduction : onnx::Constant[value={1}]
    # sum reduction : onnx::Constant[value={2}]
    reduction = symbolic_helper._maybe_get_const(reduction, "i")
    reduction_vals = ["none", "mean", "sum"]
    reduction = reduction_vals[reduction]

    # in onnx NegativeLogLikelihoodLoss specification, ignore_index is optional without default value.
    # therefore we need to set ignore_index attribute even if it is not specified (e.g. ignore_index=-100).
    ignore_index = symbolic_helper._maybe_get_const(ignore_index, "i")
    if weight.node().mustBeNone():
        nllloss = g.op(
            "NegativeLogLikelihoodLoss",
            self,
            target,
            reduction_s=reduction,
            ignore_index_i=ignore_index,
        )
    else:
        nllloss = g.op(
            "NegativeLogLikelihoodLoss",
            self,
            target,
            weight,
            reduction_s=reduction,
            ignore_index_i=ignore_index,
        )

    return nllloss

