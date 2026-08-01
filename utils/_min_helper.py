
def _min_helper(g: jit_utils.GraphContext, self, dim_or_y=None, keepdim=None):
    # torch.min(input)
    if dim_or_y is None and keepdim is None:
        return g.op("ReduceMin", self, keepdims_i=0)
    # torch.min(input, other)
    if keepdim is None:
        return _op_with_optional_float_cast(g, "Min", self, dim_or_y, opset_before=12)
    # torch.min(input, dim, keepdim)
    else:
        keepdim = _get_const(keepdim, "i", "keepdim")
        dim = _get_const(dim_or_y, "i", "dim")
        if g.opset < 18:
            min = g.op("ReduceMin", self, axes_i=[dim], keepdims_i=keepdim)
        else:
            axes = g.op("Constant", value_t=torch.tensor([dim], dtype=torch.long))
            min = g.op("ReduceMin", self, axes, keepdims_i=keepdim)
        indices = g.op("ArgMin", self, axis_i=dim, keepdims_i=keepdim)
        return min, indices

