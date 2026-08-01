
def get_constant_value(x: ir.IRNode) -> ir.Constant | None:
    """Try convert an arbitrary IR node into an ir.Constant value"""

    # First try unwrapping the IRNode to see if it is already an ir.Constant
    # Optional step, but avoids unnecessary inner_fn evaluation.
    if isinstance(x, ir.MutableBox):
        return get_constant_value(x.data)
    if isinstance(x, ir.BaseView):
        return get_constant_value(x.unwrap_view())
    if isinstance(x, ir.Constant):
        return x

    # If the unwrapped node is not an ir.Constant, try evaluating inner_fn
    # to see if the returned value is from an `ops.constant` call
    if not isinstance(x, ir.Loops):
        return None

    handler = torch._inductor.ops_handler.ExtractConstantsHandler(x.get_device())
    with (
        V.set_ops_handler(handler),
        patch.object(ir.FlexibleLayout, "allow_indexing", True),
    ):
        out = x.inner_fn(*x.inner_fn_args())

    assert isinstance(out, torch._inductor.virtualized.OpsValue)
    if isinstance(out.value, ir.Constant):
        return out.value
    return None

