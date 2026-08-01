
def _weight_norm(g: jit_utils.GraphContext, weight_v, weight_g, dim):
    rank = symbolic_helper._get_tensor_rank(weight_v)
    if rank is not None:
        # W = g * ((v) / ||v||)
        # Compute norm_except_dim for l2 norm. dim = None means over all dims
        # torch's weight_norm module sets dim = -1 if it's None.
        # This conflicts the logic for negative axes to access dims backwards
        # TODO: Might need a fix in torch group_norm module
        axes = list(range(rank))
        if dim is not None:
            if dim < -1:
                dim += rank
            if dim != -1:
                axes.remove(dim)
        norm_v = norm(g, weight_v, 2, axes, 1)
        div = g.op("Div", weight_v, norm_v)
        return g.op("Mul", div, weight_g)
    raise errors.SymbolicValueError(
        "Unsupported: ONNX export of _weight_norm for tensor of unknown rank.",
        weight_v,
    )

