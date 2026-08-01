
def inverse_trig_rule(integral: IntegralInfo, degenerate=True):
    """
    Set degenerate=False on recursive call where coefficient of quadratic term
    is assumed non-zero.
    """
    integrand, symbol = integral
    base, exp = integrand.as_base_exp()
    a = Wild('a', exclude=[symbol])
    b = Wild('b', exclude=[symbol])
    c = Wild('c', exclude=[symbol, 0])
    match = base.match(a + b*symbol + c*symbol**2)

    if not match:
        return

    def make_inverse_trig(RuleClass, a, sign_a, c, sign_c, h) -> Rule:
        u_var = Dummy("u")
        rewritten = 1/sqrt(sign_a*a + sign_c*c*(symbol-h)**2)  # a>0, c>0
        quadratic_base = sqrt(c/a)*(symbol-h)
        constant = 1/sqrt(c)
        u_func = None
        if quadratic_base is not symbol:
            u_func = quadratic_base
            quadratic_base = u_var
        standard_form = 1/sqrt(sign_a + sign_c*quadratic_base**2)
        substep = RuleClass(standard_form, quadratic_base)
        if constant != 1:
            substep = ConstantTimesRule(constant*standard_form, symbol, constant, standard_form, substep)
        if u_func is not None:
            substep = URule(rewritten, symbol, u_var, u_func, substep)
        if h != 0:
            substep = CompleteSquareRule(integrand, symbol, rewritten, substep)
        return substep

    a, b, c = [match.get(i, S.Zero) for i in (a, b, c)]
    generic_cond = Ne(c, 0)
    if not degenerate or generic_cond is S.true:
        degenerate_step = None
    elif b.is_zero:
        degenerate_step = ConstantRule(a ** exp, symbol)
    else:
        degenerate_step = sqrt_linear_rule(IntegralInfo((a + b * symbol) ** exp, symbol))

    if simplify(2*exp + 1) == 0:
        h, k = -b/(2*c), a - b**2/(4*c)  # rewrite base to k + c*(symbol-h)**2
        non_square_cond = Ne(k, 0)
        square_step = None
        if non_square_cond is not S.true:
            square_step = NestedPowRule(1/sqrt(c*(symbol-h)**2), symbol, symbol-h, S.NegativeOne)
        if non_square_cond is S.false:
            return square_step
        generic_step = ReciprocalSqrtQuadraticRule(integrand, symbol, a, b, c)
        step = _add_degenerate_step(non_square_cond, generic_step, square_step)
        if k.is_real and c.is_real:
            # list of ((rule, base_exp, a, sign_a, b, sign_b), condition)
            rules = []
            for args, cond in (  # don't apply ArccoshRule to x**2-1
                ((ArcsinRule, k, 1, -c, -1, h), And(k > 0, c < 0)),  # 1-x**2
                ((ArcsinhRule, k, 1, c, 1, h), And(k > 0, c > 0)),  # 1+x**2
            ):
                if cond is S.true:
                    return make_inverse_trig(*args)
                if cond is not S.false:
                    rules.append((make_inverse_trig(*args), cond))
            if rules:
                if not k.is_positive:  # conditions are not thorough, need fall back rule
                    rules.append((generic_step, S.true))
                step = PiecewiseRule(integrand, symbol, rules)
            else:
                step = generic_step
        return _add_degenerate_step(generic_cond, step, degenerate_step)
    if exp == S.Half:
        step = SqrtQuadraticRule(integrand, symbol, a, b, c)
        return _add_degenerate_step(generic_cond, step, degenerate_step)

