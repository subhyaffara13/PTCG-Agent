
def _diop_ternary_quadratic_normal(var, coeff):
    eq = sum(i * coeff[i] for i in coeff)
    return HomogeneousTernaryQuadraticNormal(eq, free_symbols=var).solve()

