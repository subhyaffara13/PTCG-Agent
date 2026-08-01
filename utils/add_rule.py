
def add_rule(integral):
    integrand, symbol = integral
    results = [integral_steps(g, symbol)
              for g in integrand.as_ordered_terms()]
    return None if None in results else AddRule(integrand, symbol, results)

