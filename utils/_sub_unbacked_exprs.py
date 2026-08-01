
def _sub_unbacked_exprs(shape_env: ShapeEnv, expr: sympy.Expr) -> sympy.Expr:
    """Substitute unbacked expressions with canonical equivalents.
    Used by optimization_hint to maximize consistency when hinting unbacked symbols."""
    replacements = _get_unbacked_replacements(shape_env)

    # consider making this threshold configurable
    sub_cnt_limit = 30
    sub_cnt = 0
    while sub_cnt < sub_cnt_limit:
        new_expr = expr.subs(replacements)
        if new_expr == expr:
            break
        if len(new_expr.free_symbols) <= SYMPY_FACTOR_MAX_FREE_SYMBOLS:
            expr = sympy.factor(new_expr)
        else:
            expr = new_expr
        sub_cnt += 1
    else:
        log.warning("Substitution limit (%d) reached w/ %s", sub_cnt_limit, expr)

    expr = _sympy_subs(expr, shape_env.backed_var_to_val)
    expr = _sympy_subs(expr, shape_env.var_to_hint_override)
    return expr

