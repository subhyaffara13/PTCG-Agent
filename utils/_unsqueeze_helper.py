
def _unsqueeze_helper(g: jit_utils.GraphContext, input, axes_i):
    if len(axes_i) == 0:
        # unnecessary unsqueeze if axes length==0
        return input
    elif _is_constant(axes_i[0]):
        if g.opset >= 13:
            axes = g.op("Constant", value_t=torch.tensor(axes_i, dtype=torch.long))
            return g.op("Unsqueeze", input, axes)
        return g.op("Unsqueeze", input, axes_i=axes_i)
    # Tensor type
    if g.opset < 13:
        raise errors.SymbolicValueError(
            "Opset version must be >= 13 for Unsqueeze with dynamic axes.", input
        )
    return g.op("Unsqueeze", input, axes_i[0])

