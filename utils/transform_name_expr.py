
def transform_name_expr(builder: IRBuilder, expr: NameExpr) -> Value:
    if isinstance(expr.node, TypeVarLikeExpr) and expr.node.is_new_style:
        # Reference to Python 3.12 implicit TypeVar/TupleVarTuple/... object.
        # These are stored in C statics and not visible in Python namespaces.
        return builder.load_type_var(expr.node.name, expr.node.line)
    if expr.node is None:
        builder.add(
            RaiseStandardError(
                RaiseStandardError.NAME_ERROR, f'name "{expr.name}" is not defined', expr.line
            )
        )
        return builder.none(expr.line)
    fullname = expr.node.fullname
    if builtin := builder.load_builtin(fullname, expr.line):
        return builtin
    # special cases
    if fullname == "builtins.None":
        return builder.none(expr.line)
    if fullname == "builtins.True":
        return builder.true(expr.line)
    if fullname == "builtins.False":
        return builder.false(expr.line)
    if fullname in ("typing.TYPE_CHECKING", "typing_extensions.TYPE_CHECKING"):
        return builder.false(expr.line)

    math_literal = transform_math_literal(builder, fullname, expr.line)
    if math_literal is not None:
        return math_literal

    if isinstance(expr.node, Var) and expr.node.is_final:
        final_type = builder.types.get(expr) or expr.node.type
        if final_type is None:
            final_type = AnyType(TypeOfAny.special_form)
        value = builder.emit_load_final(
            expr.node, fullname, expr.name, builder.is_native_ref_expr(expr), final_type, expr.line
        )
        if value is not None:
            return value

    if isinstance(expr.node, MypyFile) and expr.node.fullname in builder.imports:
        return builder.load_module(expr.node.fullname)

    # If the expression is locally defined, then read the result from the corresponding
    # assignment target and return it. Otherwise if the expression is a global, load it from
    # the globals dictionary.
    # Except for imports, that currently always happens in the global namespace.
    if expr.kind == LDEF and not (isinstance(expr.node, Var) and expr.node.is_suppressed_import):
        # Try to detect and error when we hit the irritating mypy bug
        # where a local variable is cast to None. (#5423)
        if (
            isinstance(expr.node, Var)
            and is_none_rprimitive(builder.node_type(expr))
            and expr.node.is_inferred
        ):
            builder.error(
                'Local variable "{}" has inferred type None; add an annotation'.format(
                    expr.node.name
                ),
                expr.node.line,
            )

        # TODO: Behavior currently only defined for Var, FuncDef and MypyFile node types.
        if isinstance(expr.node, MypyFile):
            # Load reference to a module imported inside function from
            # the modules dictionary. It would be closer to Python
            # semantics to access modules imported inside functions
            # via local variables, but this is tricky since the mypy
            # AST doesn't include a Var node for the module. We
            # instead load the module separately on each access.
            mod_dict = builder.call_c(get_module_dict_op, [], expr.line)
            obj = builder.primitive_op(
                dict_get_item_op, [mod_dict, builder.load_str(expr.node.fullname)], expr.line
            )
            return obj
        else:
            return builder.read(builder.get_assignment_target(expr, for_read=True), expr.line)

    # If we're evaluating a class body and this name is a ClassVar defined earlier
    # in the same class, load it from the class being built (type object for ext classes,
    # class dict for non-ext classes) instead of module globals.
    if (
        builder.class_body_obj is not None
        and isinstance(expr.node, Var)
        and expr.node in builder.class_body_classvars
    ):
        if builder.class_body_ir is not None and builder.class_body_ir.is_ext_class:
            return builder.py_get_attr(builder.class_body_obj, expr.name, expr.line)
        else:
            return builder.primitive_op(
                dict_get_item_op, [builder.class_body_obj, builder.load_str(expr.name)], expr.line
            )

    return builder.load_global(expr)

