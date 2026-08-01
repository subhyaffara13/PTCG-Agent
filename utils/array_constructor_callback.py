
def array_constructor_callback(ctx: mypy.plugin.FunctionContext) -> Type:
    """Callback to provide an accurate signature for the ctypes.Array constructor."""
    # Extract the element type from the constructor's return type, i. e. the type of the array
    # being constructed.
    et = _get_array_element_type(ctx.default_return_type)
    if et is not None:
        allowed = _autoconvertible_to_cdata(et, ctx.api)
        assert (
            len(ctx.arg_types) == 1
        ), "The stub of the ctypes.Array constructor should have a single vararg parameter"
        for arg_num, (arg_kind, arg_type) in enumerate(zip(ctx.arg_kinds[0], ctx.arg_types[0]), 1):
            if arg_kind == nodes.ARG_POS and not is_subtype(arg_type, allowed):
                ctx.api.msg.fail(
                    "Array constructor argument {} of type {}"
                    " is not convertible to the array element type {}".format(
                        arg_num,
                        format_type(arg_type, ctx.api.options),
                        format_type(et, ctx.api.options),
                    ),
                    ctx.context,
                )
            elif arg_kind == nodes.ARG_STAR:
                ty = ctx.api.named_generic_type("typing.Iterable", [allowed])
                if not is_subtype(arg_type, ty):
                    it = ctx.api.named_generic_type("typing.Iterable", [et])
                    ctx.api.msg.fail(
                        "Array constructor argument {} of type {}"
                        " is not convertible to the array element type {}".format(
                            arg_num,
                            format_type(arg_type, ctx.api.options),
                            format_type(it, ctx.api.options),
                        ),
                        ctx.context,
                    )

    return ctx.default_return_type

