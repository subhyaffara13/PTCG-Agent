
def _parse_converter(
    ctx: mypy.plugin.ClassDefContext, converter_expr: Expression | None
) -> Converter | None:
    """Return the Converter object from an Expression."""
    # TODO: Support complex converters, e.g. lambdas, calls, etc.
    if not converter_expr:
        return None
    converter_info = Converter()
    if (
        isinstance(converter_expr, CallExpr)
        and isinstance(converter_expr.callee, RefExpr)
        and converter_expr.callee.fullname in attr_optional_converters
        and converter_expr.args
        and converter_expr.args[0]
    ):
        # Special handling for attr.converters.optional(type)
        # We extract the type and add make the init_args Optional in Attribute.argument
        converter_expr = converter_expr.args[0]
        is_attr_converters_optional = True
    else:
        is_attr_converters_optional = False

    converter_type: Type | None = None
    if isinstance(converter_expr, RefExpr) and converter_expr.node:
        if isinstance(converter_expr.node, FuncDef):
            if converter_expr.node.type and isinstance(converter_expr.node.type, FunctionLike):
                converter_type = converter_expr.node.type
            else:  # The converter is an unannotated function.
                converter_info.init_type = AnyType(TypeOfAny.unannotated)
                return converter_info
        elif isinstance(converter_expr.node, OverloadedFuncDef) and is_valid_overloaded_converter(
            converter_expr.node
        ):
            converter_type = converter_expr.node.type
        elif isinstance(converter_expr.node, TypeInfo):
            converter_type = type_object_type(converter_expr.node)
    elif (
        isinstance(converter_expr, IndexExpr)
        and isinstance(converter_expr.analyzed, TypeApplication)
        and isinstance(converter_expr.base, RefExpr)
        and isinstance(converter_expr.base.node, TypeInfo)
    ):
        # The converter is a generic type.
        converter_type = type_object_type(converter_expr.base.node)
        if isinstance(converter_type, CallableType):
            converter_type = apply_generic_arguments(
                converter_type,
                converter_expr.analyzed.types,
                ctx.api.msg.incompatible_typevar_value,
                converter_type,
            )
        else:
            converter_type = None

    if isinstance(converter_expr, LambdaExpr):
        # TODO: should we send a fail if converter_expr.min_args > 1?
        converter_info.init_type = AnyType(TypeOfAny.unannotated)
        return converter_info

    if not converter_type:
        # Signal that we have an unsupported converter.
        ctx.api.fail(
            "Unsupported converter, only named functions, types and lambdas are currently "
            "supported",
            converter_expr,
        )
        converter_info.init_type = AnyType(TypeOfAny.from_error)
        return converter_info

    converter_type = get_proper_type(converter_type)
    if isinstance(converter_type, CallableType) and converter_type.arg_types:
        converter_info.init_type = converter_type.arg_types[0]
        if not is_attr_converters_optional:
            converter_info.ret_type = converter_type.ret_type
    elif isinstance(converter_type, Overloaded):
        types: list[Type] = []
        for item in converter_type.items:
            # Walk the overloads looking for methods that can accept one argument.
            num_arg_types = len(item.arg_types)
            if not num_arg_types:
                continue
            if num_arg_types > 1 and any(kind == ARG_POS for kind in item.arg_kinds[1:]):
                continue
            types.append(item.arg_types[0])
        # Make a union of all the valid types.
        if types:
            converter_info.init_type = make_simplified_union(types)

    if is_attr_converters_optional and converter_info.init_type:
        # If the converter was attr.converter.optional(type) then add None to
        # the allowed init_type.
        converter_info.init_type = UnionType.make_union([converter_info.init_type, NoneType()])

    return converter_info

