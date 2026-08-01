
def orthogonal_poly_rule(integral):
    orthogonal_poly_classes = {
        jacobi: JacobiRule,
        gegenbauer: GegenbauerRule,
        chebyshevt: ChebyshevTRule,
        chebyshevu: ChebyshevURule,
        legendre: LegendreRule,
        hermite: HermiteRule,
        laguerre: LaguerreRule,
        assoc_laguerre: AssocLaguerreRule
        }
    orthogonal_poly_var_index = {
        jacobi: 3,
        gegenbauer: 2,
        assoc_laguerre: 2
        }
    integrand, symbol = integral
    for klass in orthogonal_poly_classes:
        if isinstance(integrand, klass):
            var_index = orthogonal_poly_var_index.get(klass, 1)
            if (integrand.args[var_index] is symbol and not
                any(v.has(symbol) for v in integrand.args[:var_index])):
                    return orthogonal_poly_classes[klass](integrand, symbol, *integrand.args[:var_index])

