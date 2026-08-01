
def exp_rule(integral):
    integrand, symbol = integral
    if isinstance(integrand.args[0], Symbol):
        return ExpRule(integrand, symbol, E, integrand.args[0])

