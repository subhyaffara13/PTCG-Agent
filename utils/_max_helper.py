
def _max_helper(g: jit_utils.GraphContext, self, dim_or_y=None, keepdim=None):
    # torch.max(input)
    if dim_or_y is None and keepdim is None:
        return g.op("ReduceMax", self, keepdims_i=0)
    # torch.max(input, other)
    if keepdim is None:
        return _op_with_optional_float_cast(g, "Max", self, dim_or_y, opset_before=12)
    # torch.max(input, dim, keepdim)
    else:
        keepdim = _get_const(keepdim, "i", "keepdim")
        dim = _get_const(dim_or_y, "i", "dim")
        if g.opset < 18:
            max = g.op("ReduceMax", self, axes_i=[dim], keepdims_i=keepdim)
        else:
            axes = g.op("Constant", value_t=torch.tensor([dim], dtype=torch.long))
            max = g.op("ReduceMax", self, axes, keepdims_i=keepdim)
        indices = g.op("ArgMax", self, axis_i=dim, keepdims_i=keepdim)
        return max, indices

