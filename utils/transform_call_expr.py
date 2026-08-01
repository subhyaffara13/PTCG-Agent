
def transform_call_expr(builder: IRBuilder, expr: CallExpr) -> Value:
    callee = expr.callee
    if isinstance(expr.analyzed, CastExpr):
        return translate_cast_expr(builder, expr.analyzed)
    elif isinstance(expr.analyzed, AssertTypeExpr):
        # Compile to a no-op.
        return builder.accept(expr.analyzed.expr)
    elif (
        isinstance(callee, (NameExpr, MemberExpr))
        and isinstance(callee.node, TypeInfo)
        and callee.node.is_newtype
    ):
        # A call to a NewType type is a no-op at runtime.
        return builder.accept(expr.args[0])

    if isinstance(callee, IndexExpr) and isinstance(callee.analyzed, TypeApplication):
        analyzed = callee.analyzed
        if (
            isinstance(analyzed.expr, RefExpr)
            and analyzed.expr.fullname == "librt.vecs.vec"
            and len(analyzed.types) == 1
        ):
            item_type = builder.type_to_rtype(analyzed.types[0])
            vec_type = RVec(item_type)
            capacity = _get_vec_capacity(builder, expr)
            if len(expr.args) == 0 or (len(expr.args) == 1 and expr.arg_kinds == [ARG_NAMED]):
                # vec[T]() or vec[T](capacity=N)
                return vec_create(builder.builder, vec_type, 0, expr.line, capacity=capacity)
            elif (len(expr.args) == 1 and expr.arg_kinds == [ARG_POS]) or (
                len(expr.args) == 2 and expr.arg_kinds == [ARG_POS, ARG_NAMED]
            ):
                # vec[T](items) or vec[T](items, capacity=N)
                return translate_vec_create_from_iterable(
                    builder, vec_type, expr.args[0], capacity=capacity
                )
        callee = analyzed.expr  # Unwrap type application

    if isinstance(callee, MemberExpr):
        if isinstance(callee.expr, RefExpr) and isinstance(callee.expr.node, MypyFile):
            # Call a module-level function, not a method.
            return translate_call(builder, expr, callee)
        return apply_method_specialization(builder, expr, callee) or translate_method_call(
            builder, expr, callee
        )
    elif isinstance(callee, SuperExpr):
        return translate_super_method_call(builder, expr, callee)
    else:
        return translate_call(builder, expr, callee)

