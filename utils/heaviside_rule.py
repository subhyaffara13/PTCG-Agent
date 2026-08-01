
def heaviside_rule(integral):
    integrand, symbol = integral
    pattern, m, b, g = heaviside_pattern(symbol)
    match = integrand.match(pattern)
    if match and 0 != match[g]:
        # f = Heaviside(m*x + b)*g
        substep = integral_steps(match[g], symbol)
        m, b = match[m], match[b]
        return HeavisideRule(integrand, symbol, m*symbol + b, -b/m, substep)

