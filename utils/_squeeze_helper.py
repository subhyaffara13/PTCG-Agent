
def _squeeze_helper(g: jit_utils.GraphContext, input, axes_i):
    if _is_constant(axes_i[0]):
        if g.opset >= 13:
            axes = g.op("Constant", value_t=torch.tensor(axes_i, dtype=torch.long))
            return g.op("Squeeze", input, axes)
        return g.op("Squeeze", input, axes_i=axes_i)
    # Tensor type
    if g.opset < 13:
        raise errors.SymbolicValueError(
            "Opset version must be >= 13 for Squeeze with dynamic axes.", input
        )
    axes_t = axes_i[0]
    axes_rank = _get_tensor_rank(axes_t)
    if axes_rank is None:
        raise AssertionError("Expected axes_rank to be non-None")
    if axes_rank > 1:
        raise errors.SymbolicValueError(
            "For Squeeze axses as input, the axes rank must be one in ONNX spec.", input
        )
    elif axes_rank == 0:
        # The axes is a scalar. Unsqueeze it to a rank 1 tensor.
        axes_t = _unsqueeze_helper(g, axes_t, [0])
        return g.op("Squeeze", input, axes_t)
    return g.op("Squeeze", input, axes_t)

