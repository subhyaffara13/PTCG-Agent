
def trig_sindouble_rule(integral):
    integrand, symbol = integral
    a = Wild('a', exclude=[sin(2*symbol)])
    match = integrand.match(sin(2*symbol)*a)
    if match:
        sin_double = 2*sin(symbol)*cos(symbol)/sin(2*symbol)
        return integral_steps(integrand * sin_double, symbol)

