
def _get_simplified_sol(sol, func, collectterms):
    r"""
    Helper function which collects the solution on
    collectterms. Ideally this should be handled by odesimp.It is used
    only when the simplify is set to True in dsolve.

    The parameter ``collectterms`` is a list of tuple (i, reroot, imroot) where `i` is
    the multiplicity of the root, reroot is real part and imroot being the imaginary part.

    """
    f = func.func
    x = func.args[0]
    collectterms.sort(key=default_sort_key)
    collectterms.reverse()
    assert len(sol) == 1 and sol[0].lhs == f(x)
    sol = sol[0].rhs
    sol = expand_mul(sol)
    for i, reroot, imroot in collectterms:
        sol = collect(sol, x**i*exp(reroot*x)*sin(abs(imroot)*x))
        sol = collect(sol, x**i*exp(reroot*x)*cos(imroot*x))
    for i, reroot, imroot in collectterms:
        sol = collect(sol, x**i*exp(reroot*x))
    sol = powsimp(sol)
    return Eq(f(x), sol)

