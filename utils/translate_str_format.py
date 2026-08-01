
def translate_str_format(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if isinstance(callee, MemberExpr):
        folded_callee = constant_fold_expr(builder, callee.expr)
        if isinstance(folded_callee, str) and expr.arg_kinds.count(ARG_POS) == len(expr.arg_kinds):
            tokens = tokenizer_format_call(folded_callee)
            if tokens is None:
                return None
            literals, format_ops = tokens
            # Convert variables to strings
            substitutions = convert_format_expr_to_str(builder, format_ops, expr.args, expr.line)
            if substitutions is None:
                return None
            return join_formatted_strings(builder, literals, substitutions, expr.line)
    return None

