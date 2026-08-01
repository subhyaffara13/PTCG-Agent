
def translate_is_none(builder: IRBuilder, expr: Expression, negated: bool) -> Value:
    v = builder.accept(expr, can_borrow=True)
    return builder.binary_op(v, builder.none_object(), "is not" if negated else "is", expr.line)

