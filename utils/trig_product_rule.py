
def trig_product_rule(integral: IntegralInfo):
    integrand, symbol = integral
    if integrand == sec(symbol) * tan(symbol):
        return SecTanRule(integrand, symbol)
    if integrand == csc(symbol) * cot(symbol):
        return CscCotRule(integrand, symbol)

