
def precompute_set_literal(builder: IRBuilder, s: SetExpr) -> Value | None:
    """Try to pre-compute a frozenset literal during module initialization.

    Return None if it's not possible.

    Supported items:
     - Anything supported by irbuild.constant_fold.constant_fold_expr()
     - None, True, and False
     - Tuple literals with only items listed above
    """
    values = set_literal_values(builder, s.items)
    if values is not None:
        return builder.add(LoadLiteral(frozenset(values), set_rprimitive))

    return None

