
def translate_printf_style_formatting(
    builder: IRBuilder, format_expr: StrExpr | BytesExpr, rhs: Expression
) -> Value | None:
    tokens = tokenizer_printf_style(format_expr.value)
    if tokens is not None:
        literals, format_ops = tokens

        exprs = []
        if isinstance(rhs, TupleExpr):
            exprs = rhs.items
        elif isinstance(rhs, Expression):
            exprs.append(rhs)

        if isinstance(format_expr, BytesExpr):
            substitutions = convert_format_expr_to_bytes(
                builder, format_ops, exprs, format_expr.line
            )
            if substitutions is not None:
                return join_formatted_bytes(builder, literals, substitutions, format_expr.line)
        else:
            substitutions = convert_format_expr_to_str(
                builder, format_ops, exprs, format_expr.line
            )
            if substitutions is not None:
                return join_formatted_strings(builder, literals, substitutions, format_expr.line)

    return None

