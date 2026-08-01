
def binary_cross_entropy_with_logits(
    input: Tensor,
    target: Tensor,
    weight: Tensor | None = None,
    size_average: bool | None = None,
    reduce: bool | None = None,
    reduction: str = "mean",
    pos_weight: Tensor | None = None,
) -> Tensor:
    r"""Compute Binary Cross Entropy between target and input logits.

    See :class:`~torch.nn.BCEWithLogitsLoss` for details.

    Args:
        input: Tensor of arbitrary shape as unnormalized scores (often referred to as logits).
        target: Tensor of the same shape as input with values between 0 and 1
        weight (Tensor, optional): a manual rescaling weight. If provided, the dimension
           of weight supports :ref:`broadcasting to a common shape <broadcasting-semantics>`
           with respect to the input (and target) shape.
        size_average (bool, optional): Deprecated (see :attr:`reduction`).
        reduce (bool, optional): Deprecated (see :attr:`reduction`).
        reduction (str, optional): Specifies the reduction to apply to the output:
            ``'none'`` | ``'mean'`` | ``'sum'``. ``'none'``: no reduction will be applied,
            ``'mean'``: the sum of the output will be divided by the number of
            elements in the output, ``'sum'``: the output will be summed. Note: :attr:`size_average`
            and :attr:`reduce` are in the process of being deprecated, and in the meantime,
            specifying either of those two args will override :attr:`reduction`. Default: ``'mean'``
        pos_weight (Tensor, optional): a weight of positive examples to be broadcasted with target.
            Must be a tensor with equal size along the class dimension to the number of classes.
            Pay close attention to PyTorch's broadcasting semantics in order to achieve the desired
            operations. For a target of size [B, C, H, W] (where B is batch size) pos_weight of
            size [B, C, H, W] will apply different pos_weights to each element of the batch or
            [C, H, W] the same pos_weights across the batch. To apply the same positive weight
            along all spatial dimensions for a 2D multi-class target [C, H, W] use: [C, 1, 1].
            Default: ``None``

    Examples::

         >>> input = torch.randn(3, requires_grad=True)
         >>> target = torch.empty(3).random_(2)
         >>> loss = F.binary_cross_entropy_with_logits(input, target)
         >>> loss.backward()
    """
    if has_torch_function_variadic(input, target, weight, pos_weight):
        return handle_torch_function(
            binary_cross_entropy_with_logits,
            (input, target, weight, pos_weight),
            input,
            target,
            weight=weight,
            size_average=size_average,
            reduce=reduce,
            reduction=reduction,
            pos_weight=pos_weight,
        )
    if size_average is not None or reduce is not None:
        reduction_enum = _Reduction.legacy_get_enum(size_average, reduce)
    else:
        reduction_enum = _Reduction.get_enum(reduction)

    if not (target.size() == input.size()):
        raise ValueError(
            f"Target size ({target.size()}) must be the same as input size ({input.size()})"
        )

    return torch.binary_cross_entropy_with_logits(
        input, target, weight, pos_weight, reduction_enum
    )


def binary_cross_entropy_with_logits(
    self, target, weight=None, pos_weight=None, reduction=Reduction.MEAN.value
):
    if pos_weight is not None:
        log_weight = (pos_weight - 1) * target + 1
        loss = (1 - target) * self - (log_weight * F.logsigmoid(self))
    else:
        loss = (1 - target) * self - F.logsigmoid(self)

    if weight is not None:
        loss = loss * weight

    # this is to align the resulted data type with the in-place
    # operation in binary_cross_entropy_with_logits of aten/src/ATen/native/Loss.cpp
    loss = loss.to(target.dtype)
    return apply_loss_reduction(loss, reduction)


def binary_cross_entropy_with_logits(
    g: jit_utils.GraphContext, input, target, weight, pos_weight, reduction
):
    p = g.op("Constant", value_t=torch.tensor([1]))
    sig_x = opset9.sigmoid(g, input)
    log_sig_x = opset9.log(g, sig_x)
    sub_1_x = opset9.sub(g, p, sig_x)
    sub_1_y = opset9.sub(g, p, target)
    log_1_x = opset9.log(g, sub_1_x)
    if pos_weight is None or symbolic_helper._is_none(pos_weight):
        output = opset9.neg(
            g,
            opset9.add(
                g, opset9.mul(g, target, log_sig_x), opset9.mul(g, sub_1_y, log_1_x)
            ),
        )
    else:
        output = opset9.neg(
            g,
            opset9.add(
                g,
                opset9.mul(g, opset9.mul(g, target, log_sig_x), pos_weight),
                opset9.mul(g, sub_1_y, log_1_x),
            ),
        )

    if weight is not None and not symbolic_helper._is_none(weight):
        output = opset9.mul(g, weight, output)

    reduction = symbolic_helper._maybe_get_const(reduction, "i")
    if reduction == 0:
        return output
    elif reduction == 1:
        return g.op("ReduceMean", output, keepdims_i=0)
    elif reduction == 2:
        return g.op("ReduceSum", output, keepdims_i=0)
    else:
        return symbolic_helper._onnx_unsupported(
            "binary_cross_entropy_with_logits with reduction other than none, mean, or sum",
            input,
        )

