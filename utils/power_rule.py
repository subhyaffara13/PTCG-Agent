
def power_rule(integral):
    integrand, symbol = integral
    base, expt = integrand.as_base_exp()

    if symbol not in expt.free_symbols and isinstance(base, Symbol):
        if simplify(expt + 1) == 0:
            return ReciprocalRule(integrand, symbol, base)
        return PowerRule(integrand, symbol, base, expt)
    elif symbol not in base.free_symbols and isinstance(expt, Symbol):
        rule = ExpRule(integrand, symbol, base, expt)

        if fuzzy_not(log(base).is_zero):
            return rule
        elif log(base).is_zero:
            return ConstantRule(1, symbol)

        return PiecewiseRule(integrand, symbol, [
            (rule, Ne(log(base), 0)),
            (ConstantRule(1, symbol), True)
        ])

