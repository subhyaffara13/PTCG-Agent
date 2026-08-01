
def nested_pow_rule(integral: IntegralInfo):
    # nested (c*(a+b*x)**d)**e
    integrand, x = integral

    a_ = Wild('a', exclude=[x])
    b_ = Wild('b', exclude=[x, 0])
    pattern = a_+b_*x
    generic_cond = S.true

    class NoMatch(Exception):
        pass

    def _get_base_exp(expr: Expr) -> tuple[Expr, Expr]:
        if not expr.has_free(x):
            return S.One, S.Zero
        if expr.is_Mul:
            _, terms = expr.as_coeff_mul()
            if not terms:
                return S.One, S.Zero
            results = [_get_base_exp(term) for term in terms]
            bases = {b for b, _ in results}
            bases.discard(S.One)
            if len(bases) == 1:
                return bases.pop(), Add(*(e for _, e in results))
            raise NoMatch
        if expr.is_Pow:
            b, e = expr.base, expr.exp  # type: ignore
            if e.has_free(x):
                raise NoMatch
            base_, sub_exp = _get_base_exp(b)
            return base_, sub_exp * e
        match = expr.match(pattern)
        if match:
            a, b = match[a_], match[b_]
            base_ = x + a/b
            nonlocal generic_cond
            generic_cond = Ne(b, 0)
            return base_, S.One
        raise NoMatch

    try:
        base, exp_ = _get_base_exp(integrand)
    except NoMatch:
        return
    if generic_cond is S.true:
        degenerate_step = None
    else:
        # equivalent with subs(b, 0) but no need to find b
        degenerate_step = ConstantRule(integrand.subs(x, 0), x)
    generic_step = NestedPowRule(integrand, x, base, exp_)
    return _add_degenerate_step(generic_cond, generic_step, degenerate_step)

