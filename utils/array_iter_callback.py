
def array_iter_callback(ctx: mypy.plugin.MethodContext) -> Type:
    """Callback to provide an accurate return type for ctypes.Array.__iter__."""
    et = _get_array_element_type(ctx.type)
    if et is not None:
        unboxed = _autounboxed_cdata(et)
        return ctx.api.named_generic_type("typing.Iterator", [unboxed])
    return ctx.default_return_type

