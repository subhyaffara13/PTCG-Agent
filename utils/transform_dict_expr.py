
def transform_dict_expr(builder: IRBuilder, expr: DictExpr) -> Value:
    """First accepts all keys and values, then makes a dict out of them."""
    key_value_pairs = []
    for key_expr, value_expr in expr.items:
        key = builder.accept(key_expr) if key_expr is not None else None
        value = builder.accept(value_expr)
        key_value_pairs.append((key, value))

    return builder.builder.make_dict(key_value_pairs, expr.line)

