
def dirac_delta_rule(integral: IntegralInfo):
    integrand, x = integral
    if len(integrand.args) == 1:
        n = S.Zero
    else:
        n = integrand.args[1] # type: ignore
    if not n.is_Integer or n < 0:
        return
    a, b = Wild('a', exclude=[x]), Wild('b', exclude=[x, 0])
    match = integrand.args[0].match(a+b*x)
    if not match:
        return
    a, b = match[a], match[b]
    generic_cond = Ne(b, 0)
    if generic_cond is S.true:
        degenerate_step = None
    else:
        degenerate_step = ConstantRule(DiracDelta(a, n), x)
    generic_step = DiracDeltaRule(integrand, x, n, a, b)
    return _add_degenerate_step(generic_cond, generic_step, degenerate_step)

