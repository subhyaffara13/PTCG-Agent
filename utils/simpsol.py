
def simpsol(sol, wrt1, wrt2, doit=True):
    """Simplify solutions from dsolve_system."""

    # The parameter sol is the solution as returned by dsolve (list of Eq).
    #
    # The parameters wrt1 and wrt2 are lists of symbols to be collected for
    # with those in wrt1 being collected for first. This allows for collecting
    # on any factors involving the independent variable before collecting on
    # the integration constants or vice versa using e.g.:
    #
    #     sol = simpsol(sol, [t], [C1, C2])  # t first, constants after
    #     sol = simpsol(sol, [C1, C2], [t])  # constants first, t after
    #
    # If doit=True (default) then simpsol will begin by evaluating any
    # unevaluated integrals. Since many integrals will appear multiple times
    # in the solutions this is done intelligently by computing each integral
    # only once.
    #
    # The strategy is to first perform simple cancellation with factor_terms
    # and then multiply out all brackets with expand_mul. This gives an Add
    # with many terms.
    #
    # We split each term into two multiplicative factors dep and coeff where
    # all factors that involve wrt1 are in dep and any constant factors are in
    # coeff e.g.
    #         sqrt(2)*C1*exp(t) -> ( exp(t), sqrt(2)*C1 )
    #
    # The dep factors are simplified using powsimp to combine expanded
    # exponential factors e.g.
    #              exp(a*t)*exp(b*t) -> exp(t*(a+b))
    #
    # We then collect coefficients for all terms having the same (simplified)
    # dep. The coefficients are then simplified using together and ratsimp and
    # lastly by recursively applying the same transformation to the
    # coefficients to collect on wrt2.
    #
    # Finally the result is recombined into an Add and signsimp is used to
    # normalise any minus signs.

    def simprhs(rhs, rep, wrt1, wrt2):
        """Simplify the rhs of an ODE solution"""
        if rep:
            rhs = rhs.subs(rep)
        rhs = factor_terms(rhs)
        rhs = simp_coeff_dep(rhs, wrt1, wrt2)
        rhs = signsimp(rhs)
        return rhs

    def simp_coeff_dep(expr, wrt1, wrt2=None):
        """Split rhs into terms, split terms into dep and coeff and collect on dep"""
        add_dep_terms = lambda e: e.is_Add and e.has(*wrt1)
        expandable = lambda e: e.is_Mul and any(map(add_dep_terms, e.args))
        expand_func = lambda e: expand_mul(e, deep=False)
        expand_mul_mod = lambda e: e.replace(expandable, expand_func)
        terms = Add.make_args(expand_mul_mod(expr))
        dc = {}
        for term in terms:
            coeff, dep = term.as_independent(*wrt1, as_Add=False)
            # Collect together the coefficients for terms that have the same
            # dependence on wrt1 (after dep is normalised using simpdep).
            dep = simpdep(dep, wrt1)

            # See if the dependence on t cancels out...
            if dep is not S.One:
                dep2 = factor_terms(dep)
                if not dep2.has(*wrt1):
                    coeff *= dep2
                    dep = S.One

            if dep not in dc:
                dc[dep] = coeff
            else:
                dc[dep] += coeff
        # Apply the method recursively to the coefficients but this time
        # collecting on wrt2 rather than wrt2.
        termpairs = ((simpcoeff(c, wrt2), d) for d, c in dc.items())
        if wrt2 is not None:
            termpairs = ((simp_coeff_dep(c, wrt2), d) for c, d in termpairs)
        return Add(*(c * d for c, d in termpairs))

    def simpdep(term, wrt1):
        """Normalise factors involving t with powsimp and recombine exp"""
        def canonicalise(a):
            # Using factor_terms here isn't quite right because it leads to things
            # like exp(t*(1+t)) that we don't want. We do want to cancel factors
            # and pull out a common denominator but ideally the numerator would be
            # expressed as a standard form polynomial in t so we expand_mul
            # and collect afterwards.
            a = factor_terms(a)
            num, den = a.as_numer_denom()
            num = expand_mul(num)
            num = collect(num, wrt1)
            return num / den

        term = powsimp(term)
        rep = {e: exp(canonicalise(e.args[0])) for e in term.atoms(exp)}
        term = term.subs(rep)
        return term

    def simpcoeff(coeff, wrt2):
        """Bring to a common fraction and cancel with ratsimp"""
        coeff = together(coeff)
        if coeff.is_polynomial():
            # Calling ratsimp can be expensive. The main reason is to simplify
            # sums of terms with irrational denominators so we limit ourselves
            # to the case where the expression is polynomial in any symbols.
            # Maybe there's a better approach...
            coeff = ratsimp(radsimp(coeff))
        # collect on secondary variables first and any remaining symbols after
        if wrt2 is not None:
            syms = list(wrt2) + list(ordered(coeff.free_symbols - set(wrt2)))
        else:
            syms = list(ordered(coeff.free_symbols))
        coeff = collect(coeff, syms)
        coeff = together(coeff)
        return coeff

    # There are often repeated integrals. Collect unique integrals and
    # evaluate each once and then substitute into the final result to replace
    # all occurrences in each of the solution equations.
    if doit:
        integrals = set().union(*(s.atoms(Integral) for s in sol))
        rep = {i: factor_terms(i).doit() for i in integrals}
    else:
        rep = {}

    sol = [Eq(s.lhs, simprhs(s.rhs, rep, wrt1, wrt2)) for s in sol]
    return sol

