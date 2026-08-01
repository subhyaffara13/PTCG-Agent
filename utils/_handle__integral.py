
def _handle_Integral(expr, func, order, hint):
    r"""
    Converts a solution with integrals in it into an actual solution.

    Simplifies the integral mainly using doit()
    """
    if hint.endswith("_Integral"):
        return expr

    elif hint == "1st_linear_constant_coeff":
        return simplify(expr.doit())

    else:
        return expr


def _handle_Integral(expr, func, hint):
    r"""
    Converts a solution with Integrals in it into an actual solution.

    For most hints, this simply runs ``expr.doit()``.

    """
    if hint == "nth_linear_constant_coeff_homogeneous":
        sol = expr
    elif not hint.endswith("_Integral"):
        sol = expr.doit()
    else:
        sol = expr
    return sol

