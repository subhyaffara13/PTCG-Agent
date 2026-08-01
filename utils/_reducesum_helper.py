
def _reducesum_helper(
    g: jit_utils.GraphContext,
    input,
    axes_i=None,
    keepdims_i=1,
    noop_with_empty_axes_i=0,
):
    keepdims_i = _maybe_get_const(keepdims_i, "i")
    if g.opset >= 13:
        if axes_i:
            if not _is_value(axes_i):
                axes_i = g.op(
                    "Constant", value_t=torch.tensor(axes_i, dtype=torch.long)
                )
            return g.op(
                "ReduceSum",
                input,
                axes_i,
                keepdims_i=keepdims_i,
                noop_with_empty_axes_i=noop_with_empty_axes_i,
            )
        return g.op(
            "ReduceSum",
            input,
            keepdims_i=keepdims_i,
            noop_with_empty_axes_i=noop_with_empty_axes_i,
        )
    else:
        return g.op("ReduceSum", input, axes_i=axes_i, keepdims_i=keepdims_i)

