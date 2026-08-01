
def prim_tolist(g: jit_utils.GraphContext, input, dim_val, elem_ty_val):
    """tolist is currently supported only for 1D input tensors.

    dim_val and elem_ty_val represent dimension and type annotations
    that need to match dimension and type of the input tensor.
    """
    dim = symbolic_helper._maybe_get_const(dim_val, "i")
    if dim > 1:
        return symbolic_helper._unimplemented("prim::tolist", "dim_val > 1", input)
    return input

