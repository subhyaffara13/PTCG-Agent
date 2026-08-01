
def _simplify_variable_coeff(sol, syms, func, funcarg):
    r"""
    Helper function to replace constants by functions in 1st_linear_variable_coeff
    """
    eta = Symbol("eta")
    if len(syms) == 1:
        sym = syms.pop()
        final = sol.subs(sym, func(funcarg))

    else:
        for sym in syms:
            final = sol.subs(sym, func(funcarg))

    return simplify(final.subs(eta, funcarg))

