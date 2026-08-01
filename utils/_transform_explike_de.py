
def _transform_explike_DE(DE, g, x, order, syms):
    """Converts DE with free parameters into DE with constant coefficients."""
    from sympy.solvers.solveset import linsolve

    eq = []
    highest_coeff = DE.coeff(Derivative(g(x), x, order))
    for i in range(order):
        coeff = DE.coeff(Derivative(g(x), x, i))
        coeff = (coeff / highest_coeff).expand().collect(x)
        eq.extend(Add.make_args(coeff))
    temp = []
    for e in eq:
        if e.has(x):
            break
        elif e.has(Symbol):
            temp.append(e)
    else:
        eq = temp
    if eq:
        sol = dict(zip(syms, (i for s in linsolve(eq, list(syms)) for i in s)))
        if sol:
            DE = DE.subs(sol)
            DE = DE.factor().as_coeff_mul(Derivative)[1][0]
            DE = DE.collect(Derivative(g(x)))
    return DE

