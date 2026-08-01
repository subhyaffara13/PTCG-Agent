
def array_value_callback(ctx: mypy.plugin.AttributeContext) -> Type:
    """Callback to provide an accurate type for ctypes.Array.value."""
    et = _get_array_element_type(ctx.type)
    if et is not None:
        types: list[Type] = []
        for tp in flatten_nested_unions([et]):
            tp = get_proper_type(tp)
            if isinstance(tp, AnyType):
                types.append(AnyType(TypeOfAny.from_another_any, source_any=tp))
            elif isinstance(tp, Instance) and tp.type.fullname == "ctypes.c_char":
                types.append(ctx.api.named_generic_type("builtins.bytes", []))
            elif isinstance(tp, Instance) and tp.type.fullname == "ctypes.c_wchar":
                types.append(ctx.api.named_generic_type("builtins.str", []))
            else:
                ctx.api.msg.fail(
                    'Array attribute "value" is only available'
                    ' with element type "c_char" or "c_wchar", not {}'.format(
                        format_type(et, ctx.api.options)
                    ),
                    ctx.context,
                )
        return make_simplified_union(types)
    return ctx.default_attr_type

