
def cross_entropy_loss(
    self: list[int],
    target: list[int],
    weight: Optional[list[int]] = None,
    reduction: int = 1,
    ignore_index: int = -100,
    label_smoothing: float = 0.0,
) -> list[int]:
    result_shape = nll_loss_forward(self, target, weight, reduction)[0]
    return result_shape


def cross_entropy_loss(
    g: jit_utils.GraphContext,
    self,
    target,
    weight,
    reduction,
    ignore_index,
    label_smoothing,
):
    # none reduction : onnx::Constant[value={0}]
    # mean reduction : onnx::Constant[value={1}]
    # sum reduction : onnx::Constant[value={2}]
    reduction = symbolic_helper._maybe_get_const(reduction, "i")
    reduction_vals = ["none", "mean", "sum"]
    reduction = reduction_vals[reduction]

    label_smoothing = symbolic_helper._maybe_get_const(label_smoothing, "f")
    if label_smoothing is not None and label_smoothing > 0.0:
        raise errors.SymbolicValueError(
            "Unsupported: ONNX does not support label_smoothing", self
        )

    # in onnx SoftmaxCrossEntropyLoss specification, ignore_index is optional without default value.
    # therefore we need to set ignore_index attribute even if it is not specified (e.g. ignore_index=-100).
    ignore_index = symbolic_helper._maybe_get_const(ignore_index, "i")
    if weight.node().mustBeNone():
        celoss = g.op(
            "SoftmaxCrossEntropyLoss",
            self,
            target,
            reduction_s=reduction,
            ignore_index_i=ignore_index,
        )
    else:
        celoss = g.op(
            "SoftmaxCrossEntropyLoss",
            self,
            target,
            weight,
            reduction_s=reduction,
            ignore_index_i=ignore_index,
        )

    return celoss

