
def canonicalize_bool_expr(expr: _T) -> _T:
    """
    Canonicalize a boolean expression by transforming it into a lt / le
    inequality and moving all the non-constant terms to the rhs.
    We canonicalize And / Ors / Not via cnf and then canonicalize their subexpr
    recursively
    nb. sympy.Rel.canonical is not good enough https://github.com/sympy/sympy/issues/25924

    Args:
        expr (sympy.Expr): Expression to canonicalize
    """
    # Canonicalise an inequality by transforming it into a lt / le
    # inequality and moving all the non-constant terms to the rhs
    # We canonicalise And / Ors / Not via cnf
    # nb. Relational.canonical in sympy is broken
    # https://github.com/sympy/sympy/issues/25924

    if not isinstance(
        expr, (sympy.Rel, sympy.And, sympy.Or, sympy.Not, sympy.Eq, sympy.Ne)
    ):
        return expr

    if isinstance(expr, (sympy.And, sympy.Or, sympy.Not)):
        expr = sympy.logic.boolalg.to_cnf(expr)
    return _canonicalize_bool_expr_impl(expr)  # type: ignore[arg-type, return-value]

