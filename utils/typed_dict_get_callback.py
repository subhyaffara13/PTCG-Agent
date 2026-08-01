
def typed_dict_get_callback(ctx: MethodContext) -> Type:
    """Infer a precise return type for TypedDict.get with literal first argument."""
    if (
        isinstance(ctx.type, TypedDictType)
        and len(ctx.arg_types) >= 1
        and len(ctx.arg_types[0]) == 1
    ):
        keys = try_getting_str_literals(ctx.args[0][0], ctx.arg_types[0][0])
        if keys is None:
            return ctx.default_return_type

        default_type: Type
        default_arg: Expression | None
        if len(ctx.arg_types) <= 1 or not ctx.arg_types[1]:
            default_arg = None
            default_type = NoneType()
        elif len(ctx.arg_types[1]) == 1 and len(ctx.args[1]) == 1:
            default_arg = ctx.args[1][0]
            default_type = ctx.arg_types[1][0]
        else:
            return ctx.default_return_type

        output_types: list[Type] = []
        for key in keys:
            value_type: Type | None = ctx.type.items.get(key)
            if value_type is None:
                if not ctx.type.is_closed:
                    return ctx.default_return_type
                output_types.append(default_type)
            elif key in ctx.type.required_keys:
                output_types.append(value_type)
            else:
                # HACK to deal with get(key, {})
                if (
                    isinstance(default_arg, DictExpr)
                    and len(default_arg.items) == 0
                    and isinstance(vt := get_proper_type(value_type), TypedDictType)
                ):
                    output_types.append(vt.copy_modified(required_keys=set()))
                else:
                    output_types.append(value_type)
                    output_types.append(default_type)

        # for nicer reveal_type, put default at the end, if it is present
        if default_type in output_types:
            output_types = [t for t in output_types if t != default_type] + [default_type]
        return make_simplified_union(output_types)
    return ctx.default_return_type

