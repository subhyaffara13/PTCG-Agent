
def fields_function_sig_callback(ctx: mypy.plugin.FunctionSigContext) -> CallableType:
    """Provide the signature for `attrs.fields`."""
    if len(ctx.args) != 1 or len(ctx.args[0]) != 1:
        return ctx.default_signature

    proper_type = get_proper_type(ctx.api.get_expression_type(ctx.args[0][0]))

    # fields(Any) -> Any, fields(type[Any]) -> Any
    if (
        isinstance(proper_type, AnyType)
        or isinstance(proper_type, TypeType)
        and isinstance(proper_type.item, AnyType)
    ):
        return ctx.default_signature

    cls = None
    arg_types = ctx.default_signature.arg_types

    if isinstance(proper_type, TypeVarType):
        inner = get_proper_type(proper_type.upper_bound)
        if isinstance(inner, Instance):
            # We need to work arg_types to compensate for the attrs stubs.
            arg_types = [proper_type]
            cls = inner.type
    elif isinstance(proper_type, CallableType):
        cls = proper_type.type_object()

    if cls is not None and MAGIC_ATTR_NAME in cls.names:
        # This is a proper attrs class.
        ret_type = cls.names[MAGIC_ATTR_NAME].type
        assert ret_type is not None
        return ctx.default_signature.copy_modified(arg_types=arg_types, ret_type=ret_type)

    return ctx.default_signature

