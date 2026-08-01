
def constant_fold_expr(expr: Expression, cur_mod_id: str) -> ConstantValue | None:
    """Return the constant value of an expression for supported operations.

    Among other things, support int arithmetic and string
    concatenation. For example, the expression 3 + 5 has the constant
    value 8.

    Also bind simple references to final constants defined in the
    current module (cur_mod_id). Binding to references is best effort
    -- we don't bind references to other modules. Mypyc trusts these
    to be correct in compiled modules, so that it can replace a
    constant expression (or a reference to one) with the statically
    computed value. We don't want to infer constant values based on
    stubs, in particular, as these might not match the implementation
    (due to version skew, for example).

    Return None if unsuccessful.
    """
    if isinstance(expr, IntExpr):
        return expr.value
    if isinstance(expr, StrExpr):
        return expr.value
    if isinstance(expr, FloatExpr):
        return expr.value
    if isinstance(expr, ComplexExpr):
        return expr.value
    elif isinstance(expr, NameExpr):
        if expr.name == "True":
            return True
        elif expr.name == "False":
            return False
        node = expr.node
        if (
            isinstance(node, Var)
            and node.is_final
            and node.fullname.rsplit(".", 1)[0] == cur_mod_id
        ):
            value = node.final_value
            if isinstance(value, (CONST_TYPES)):
                return value
    elif isinstance(expr, OpExpr):
        left = constant_fold_expr(expr.left, cur_mod_id)
        right = constant_fold_expr(expr.right, cur_mod_id)
        if left is not None and right is not None:
            return constant_fold_binary_op(expr.op, left, right)
    elif isinstance(expr, UnaryExpr):
        value = constant_fold_expr(expr.expr, cur_mod_id)
        if value is not None:
            return constant_fold_unary_op(expr.op, value)
    return None


def constant_fold_expr(builder: IRBuilder, expr: Expression) -> ConstantValue | None:
    """Return the constant value of an expression for supported operations.

    Return None otherwise.
    """
    if isinstance(expr, IntExpr):
        return expr.value
    if isinstance(expr, FloatExpr):
        return expr.value
    if isinstance(expr, StrExpr):
        return expr.value
    if isinstance(expr, BytesExpr):
        return bytes_from_str(expr.value)
    if isinstance(expr, ComplexExpr):
        return expr.value
    elif isinstance(expr, NameExpr):
        node = expr.node
        if isinstance(node, Var) and node.is_final:
            final_value = node.final_value
            if isinstance(final_value, (CONST_TYPES)):
                return final_value
    elif isinstance(expr, MemberExpr):
        final = builder.get_final_ref(expr)
        if final is not None:
            fn, final_var, native = final
            if final_var.is_final:
                final_value = final_var.final_value
                if isinstance(final_value, (CONST_TYPES)):
                    return final_value
    elif isinstance(expr, OpExpr):
        left = constant_fold_expr(builder, expr.left)
        right = constant_fold_expr(builder, expr.right)
        if left is not None and right is not None:
            return constant_fold_binary_op_extended(expr.op, left, right)
    elif isinstance(expr, UnaryExpr):
        value = constant_fold_expr(builder, expr.expr)
        if value is not None and not isinstance(value, bytes):
            return constant_fold_unary_op(expr.op, value)
    return None

