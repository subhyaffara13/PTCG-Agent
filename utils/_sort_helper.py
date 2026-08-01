
def _sort_helper(tensor, axis, kind, order):
    if tensor.dtype.is_complex:
        raise NotImplementedError(f"sorting {tensor.dtype} is not supported")
    (tensor,), axis = _util.axis_none_flatten(tensor, axis=axis)
    axis = _util.normalize_axis_index(axis, tensor.ndim)

    stable = kind == "stable"

    return tensor, axis, stable


def _sort_helper(g: jit_utils.GraphContext, input, dim, descending=True, out=None):
    if out is not None:
        _unimplemented("Sort", "Out parameter is not supported")
    shape_ = g.op("Shape", input)
    dim_size_ = g.op(
        "Gather",
        shape_,
        g.op("Constant", value_t=torch.tensor([dim], dtype=torch.int64)),
    )
    if g.opset <= 10:
        if not descending:
            _unimplemented("Sort", "Ascending is not supported")
        return g.op("TopK", input, dim_size_, axis_i=dim, outputs=2)
    else:
        return g.op(
            "TopK", input, dim_size_, axis_i=dim, largest_i=descending, outputs=2
        )

