
def array_getitem_callback(ctx: mypy.plugin.MethodContext) -> Type:
    """Callback to provide an accurate return type for ctypes.Array.__getitem__."""
    et = _get_array_element_type(ctx.type)
    if et is not None:
        unboxed = _autounboxed_cdata(et)
        assert (
            len(ctx.arg_types) == 1
        ), "The stub of ctypes.Array.__getitem__ should have exactly one parameter"
        assert (
            len(ctx.arg_types[0]) == 1
        ), "ctypes.Array.__getitem__'s parameter should not be variadic"
        index_type = get_proper_type(ctx.arg_types[0][0])
        if isinstance(index_type, Instance):
            if index_type.type.has_base("builtins.int"):
                return unboxed
            elif index_type.type.has_base("builtins.slice"):
                return ctx.api.named_generic_type("builtins.list", [unboxed])
    return ctx.default_return_type

