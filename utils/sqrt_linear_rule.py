
def sqrt_linear_rule(integral: IntegralInfo):
    """
    Substitute common (a+b*x)**(1/n)
    """
    integrand, x = integral
    a = Wild('a', exclude=[x])
    b = Wild('b', exclude=[x, 0])
    a0 = b0 = 0
    bases, qs, bs = [], [], []
    for pow_ in integrand.find(Pow):  # collect all (a+b*x)**(p/q)
        base, exp_ = pow_.base, pow_.exp
        if exp_.is_Integer or x not in base.free_symbols:  # skip 1/x and sqrt(2)
            continue
        if not exp_.is_Rational:  # exclude x**pi
            return
        match = base.match(a+b*x)
        if not match:  # skip non-linear
            continue  # for sqrt(x+sqrt(x)), although base is non-linear, we can still substitute sqrt(x)
        a1, b1 = match[a], match[b]
        if a0*b1 != a1*b0 or not (b0/b1).is_nonnegative:  # cannot transform sqrt(x) to sqrt(x+1) or sqrt(-x)
            return
        if b0 == 0 or (b0/b1 > 1) is S.true:  # choose the latter of sqrt(2*x) and sqrt(x) as representative
            a0, b0 = a1, b1
        bases.append(base)
        bs.append(b1)
        qs.append(exp_.q)
    if b0 == 0:  # no such pattern found
        return
    q0: Integer = lcm_list(qs)
    u_x = (a0 + b0*x)**(1/q0)
    u = Dummy("u")
    substituted = integrand.subs({base**(S.One/q): (b/b0)**(S.One/q)*u**(q0/q)
                                  for base, b, q in zip(bases, bs, qs)}).subs(x, (u**q0-a0)/b0)
    substep = integral_steps(substituted*u**(q0-1)*q0/b0, u)
    if not substep.contains_dont_know():
        step: Rule = URule(integrand, x, u, u_x, substep)
        generic_cond = Ne(b0, 0)
        if generic_cond is not S.true:  # possible degenerate case
            simplified = integrand.subs(dict.fromkeys(bs, 0))
            degenerate_step = integral_steps(simplified, x)
            step = PiecewiseRule(integrand, x, [(step, generic_cond), (degenerate_step, S.true)])
        return step

