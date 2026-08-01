
def _simpsol(soleq):
    lhs = soleq.lhs
    sol = soleq.rhs
    sol = powsimp(sol)
    gens = list(sol.atoms(exp))
    p = Poly(sol, *gens, expand=False)
    gens = [factor_terms(g) for g in gens]
    if not gens:
        gens = p.gens
    syms = [Symbol('C1'), Symbol('C2')]
    terms = []
    for coeff, monom in zip(p.coeffs(), p.monoms()):
        coeff = piecewise_fold(coeff)
        if isinstance(coeff, Piecewise):
            coeff = Piecewise(*((ratsimp(coef).collect(syms), cond) for coef, cond in coeff.args))
        else:
            coeff = ratsimp(coeff).collect(syms)
        monom = Mul(*(g ** i for g, i in zip(gens, monom)))
        terms.append(coeff * monom)
    return Eq(lhs, Add(*terms))

