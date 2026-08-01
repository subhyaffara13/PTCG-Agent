
def mul_rule(integral: IntegralInfo):
    integrand, symbol = integral

    # Constant times function case
    coeff, f = integrand.as_independent(symbol)
    if coeff != 1:
        next_step = integral_steps(f, symbol)
        if next_step is not None:
            return ConstantTimesRule(integrand, symbol, coeff, f, next_step)

