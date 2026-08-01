
def translate_fstring(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    """Special case for f-string, which is translated into str.join()
    in mypy AST.

    This specializer optimizes simplest f-strings which don't contain
    any format operation.
    """
    if (
        isinstance(callee, MemberExpr)
        and isinstance(callee.expr, StrExpr)
        and callee.expr.value == ""
        and expr.arg_kinds == [ARG_POS]
        and isinstance(expr.args[0], ListExpr)
    ):
        for item in expr.args[0].items:
            if isinstance(item, StrExpr):
                continue
            elif isinstance(item, CallExpr):
                if not isinstance(item.callee, MemberExpr) or item.callee.name != "format":
                    return None
                elif (
                    not isinstance(item.callee.expr, StrExpr) or item.callee.expr.value != "{:{}}"
                ):
                    return None

                if not isinstance(item.args[1], StrExpr) or item.args[1].value != "":
                    return None
            else:
                return None

        format_ops = []
        exprs: list[Expression] = []

        for item in expr.args[0].items:
            if isinstance(item, StrExpr) and item.value != "":
                format_ops.append(FormatOp.STR)
                exprs.append(item)
            elif isinstance(item, CallExpr):
                format_ops.append(FormatOp.STR)
                exprs.append(item.args[0])

        def get_literal_str(expr: Expression) -> str | None:
            if isinstance(expr, StrExpr):
                return expr.value
            elif isinstance(expr, RefExpr) and isinstance(expr.node, Var) and expr.node.is_final:
                final_value = expr.node.final_value
                if final_value is not None:
                    return str(final_value)
            return None

        for i in range(len(exprs) - 1):
            while (
                len(exprs) >= i + 2
                and (first := get_literal_str(exprs[i])) is not None
                and (second := get_literal_str(exprs[i + 1])) is not None
            ):
                exprs = [*exprs[:i], StrExpr(first + second), *exprs[i + 2 :]]
                format_ops = [*format_ops[:i], FormatOp.STR, *format_ops[i + 2 :]]

        substitutions = convert_format_expr_to_str(builder, format_ops, exprs, expr.line)
        if substitutions is None:
            return None

        return join_formatted_strings(builder, None, substitutions, expr.line)
    return None

