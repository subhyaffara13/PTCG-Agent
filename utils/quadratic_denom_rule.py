
def quadratic_denom_rule(integral):
    integrand, symbol = integral
    a = Wild('a', exclude=[symbol])
    b = Wild('b', exclude=[symbol])
    c = Wild('c', exclude=[symbol])

    match = integrand.match(a / (b * symbol ** 2 + c))

    if match:
        a, b, c = match[a], match[b], match[c]
        general_rule = ArctanRule(integrand, symbol, a, b, c)
        if b.is_extended_real and c.is_extended_real:
            positive_cond = c/b > 0
            if positive_cond is S.true:
                return general_rule
            coeff = a/(2*sqrt(-c)*sqrt(b))
            constant = sqrt(-c/b)
            r1 = 1/(symbol-constant)
            r2 = 1/(symbol+constant)
            log_steps = [ReciprocalRule(r1, symbol, symbol-constant),
                         ConstantTimesRule(-r2, symbol, -1, r2, ReciprocalRule(r2, symbol, symbol+constant))]
            rewritten = sub = r1 - r2
            negative_step = AddRule(sub, symbol, log_steps)
            if coeff != 1:
                rewritten = Mul(coeff, sub, evaluate=False)
                negative_step = ConstantTimesRule(rewritten, symbol, coeff, sub, negative_step)
            negative_step = RewriteRule(integrand, symbol, rewritten, negative_step)
            if positive_cond is S.false:
                return negative_step
            return PiecewiseRule(integrand, symbol, [(general_rule, positive_cond), (negative_step, S.true)])

        power = PowerRule(integrand, symbol, symbol, -2)
        if b != 1:
            power = ConstantTimesRule(integrand, symbol, 1/b, symbol**-2, power)

        return PiecewiseRule(integrand, symbol, [(general_rule, Ne(c, 0)), (power, True)])

    d = Wild('d', exclude=[symbol])
    match2 = integrand.match(a / (b * symbol ** 2 + c * symbol + d))
    if match2:
        b, c =  match2[b], match2[c]
        if b.is_zero:
            return
        u = Dummy('u')
        u_func = symbol + c/(2*b)
        integrand2 = integrand.subs(symbol, u - c / (2*b))
        next_step = integral_steps(integrand2, u)
        if next_step:
            return URule(integrand2, symbol, u, u_func, next_step)
        else:
            return
    e = Wild('e', exclude=[symbol])
    match3 = integrand.match((a* symbol + b) / (c * symbol ** 2 + d * symbol + e))
    if match3:
        a, b, c, d, e = match3[a], match3[b], match3[c], match3[d], match3[e]
        if c.is_zero:
            return
        denominator = c * symbol**2 + d * symbol + e
        const =  a/(2*c)
        numer1 =  (2*c*symbol+d)
        numer2 = - const*d + b
        u = Dummy('u')
        step1 = URule(integrand, symbol,
                      u, denominator, integral_steps(u**(-1), u))
        if const != 1:
            step1 = ConstantTimesRule(const*numer1/denominator, symbol,
                                      const, numer1/denominator, step1)
        if numer2.is_zero:
            return step1
        step2 = integral_steps(numer2/denominator, symbol)
        substeps = AddRule(integrand, symbol, [step1, step2])
        rewriten = const*numer1/denominator+numer2/denominator
        return RewriteRule(integrand, symbol, rewriten, substeps)

    return

