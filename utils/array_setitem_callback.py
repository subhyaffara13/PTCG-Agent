
def array_setitem_callback(ctx: mypy.plugin.MethodSigContext) -> CallableType:
    """Callback to provide an accurate signature for ctypes.Array.__setitem__."""
    et = _get_array_element_type(ctx.type)
    if et is not None:
        allowed = _autoconvertible_to_cdata(et, ctx.api)
        assert len(ctx.default_signature.arg_types) == 2
        index_type = get_proper_type(ctx.default_signature.arg_types[0])
        if isinstance(index_type, Instance):
            arg_type = None
            if index_type.type.has_base("builtins.int"):
                arg_type = allowed
            elif index_type.type.has_base("builtins.slice"):
                arg_type = ctx.api.named_generic_type("builtins.list", [allowed])
            if arg_type is not None:
                # Note: arg_type can only be None if index_type is invalid, in which case we use
                # the default signature and let mypy report an error about it.
                return ctx.default_signature.copy_modified(
                    arg_types=ctx.default_signature.arg_types[:1] + [arg_type]
                )
    return ctx.default_signature

