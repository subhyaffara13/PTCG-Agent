
def transform_op_expr(builder: IRBuilder, expr: OpExpr) -> Value:
    if expr.op in ("and", "or"):
        return builder.shortcircuit_expr(expr)

    # Special case for string formatting
    if expr.op == "%" and isinstance(expr.left, (StrExpr, BytesExpr)):
        ret = translate_printf_style_formatting(builder, expr.left, expr.right)
        if ret is not None:
            return ret

    folded = try_constant_fold(builder, expr)
    if folded:
        return folded

    borrow_left = False
    borrow_right = False

    ltype = builder.node_type(expr.left)
    rtype = builder.node_type(expr.right)

    # Special case some int ops to allow borrowing operands.
    if is_int_rprimitive(ltype) and is_int_rprimitive(rtype):
        if expr.op == "//":
            expr = try_optimize_int_floor_divide(builder, expr)
        if expr.op in int_borrow_friendly_op:
            borrow_left = is_borrow_friendly_expr(builder, expr.right)
            borrow_right = True
    elif is_fixed_width_rtype(ltype) and is_fixed_width_rtype(rtype):
        borrow_left = is_borrow_friendly_expr(builder, expr.right)
        borrow_right = True

    left = builder.accept(expr.left, can_borrow=borrow_left)
    right = builder.accept(expr.right, can_borrow=borrow_right)
    return builder.binary_op(left, right, expr.op, expr.line)

