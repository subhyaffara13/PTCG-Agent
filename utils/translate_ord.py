
def translate_ord(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if len(expr.args) != 1 or expr.arg_kinds[0] != ARG_POS:
        return None
    arg_expr = expr.args[0]
    arg = constant_fold_expr(builder, arg_expr)
    if isinstance(arg, (str, bytes)) and len(arg) == 1:
        return Integer(ord(arg))

    # Check for ord(s[i]) where s is str and i is an integer
    if isinstance(arg_expr, IndexExpr):
        # Check base type
        base_type = builder.node_type(arg_expr.base)
        if is_str_rprimitive(base_type):
            # Check index type
            index_expr = arg_expr.index
            index_type = builder.node_type(index_expr)
            if is_tagged(index_type) or is_fixed_width_rtype(index_type):
                # This is ord(s[i]) where s is str and i is an integer.
                # Generate specialized inline code using the helper.
                result = translate_getitem_with_bounds_check(
                    builder,
                    arg_expr.base,
                    [arg_expr.index],
                    expr,
                    str_adjust_index_op,
                    str_range_check_op,
                    str_get_item_unsafe_as_int_op,
                )
                return result

    return None

