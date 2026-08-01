
def solve_triangulated(polys, *gens, **args):
    """
    Solve a polynomial system using Gianni-Kalkbrenner algorithm.

    The algorithm proceeds by computing one Groebner basis in the ground
    domain and then by iteratively computing polynomial factorizations in
    appropriately constructed algebraic extensions of the ground domain.

    Parameters
    ==========

    polys: a list/tuple/set
        Listing all the equations that are needed to be solved
    gens: generators
        generators of the equations in polys for which we want the
        solutions
    args: Keyword arguments
        Special options for solving the equations

    Returns
    =======

    List[Tuple]
        A List of tuples. Solutions for symbols that satisfy the
        equations listed in polys

    Examples
    ========

    >>> from sympy import solve_triangulated
    >>> from sympy.abc import x, y, z

    >>> F = [x**2 + y + z - 1, x + y**2 + z - 1, x + y + z**2 - 1]

    >>> solve_triangulated(F, x, y, z)
    [(0, 0, 1), (0, 1, 0), (1, 0, 0)]

    Using extension for algebraic solutions.

    >>> solve_triangulated(F, x, y, z, extension=True) #doctest: +NORMALIZE_WHITESPACE
    [(0, 0, 1), (0, 1, 0), (1, 0, 0),
     (CRootOf(x**2 + 2*x - 1, 0), CRootOf(x**2 + 2*x - 1, 0), CRootOf(x**2 + 2*x - 1, 0)),
     (CRootOf(x**2 + 2*x - 1, 1), CRootOf(x**2 + 2*x - 1, 1), CRootOf(x**2 + 2*x - 1, 1))]

    References
    ==========

    1. Patrizia Gianni, Teo Mora, Algebraic Solution of System of
    Polynomial Equations using Groebner Bases, AAECC-5 on Applied Algebra,
    Algebraic Algorithms and Error-Correcting Codes, LNCS 356 247--257, 1989

    """
    opt = build_options(gens, args)

    G = groebner(polys, gens, polys=True)
    G = list(reversed(G))

    extension = opt.get('extension', False)
    if extension:
        def _solve_univariate(f):
            return [r for r, _ in f.all_roots(multiple=False, radicals=False)]
    else:
        domain = opt.get('domain')

        if domain is not None:
            for i, g in enumerate(G):
                G[i] = g.set_domain(domain)

        def _solve_univariate(f):
            return list(f.ground_roots().keys())

    f, G = G[0].ltrim(-1), G[1:]
    dom = f.get_domain()

    zeros = _solve_univariate(f)

    if extension:
        solutions = {((zero,), dom.algebraic_field(zero)) for zero in zeros}
    else:
        solutions = {((zero,), dom) for zero in zeros}

    var_seq = reversed(gens[:-1])
    vars_seq = postfixes(gens[1:])

    for var, vars in zip(var_seq, vars_seq):
        _solutions = set()

        for values, dom in solutions:
            H, mapping = [], list(zip(vars, values))

            for g in G:
                _vars = (var,) + vars

                if g.has_only_gens(*_vars) and g.degree(var) != 0:
                    if extension:
                        g = g.set_domain(g.domain.unify(dom))
                    h = g.ltrim(var).eval(dict(mapping))

                    if g.degree(var) == h.degree():
                        H.append(h)

            p = min(H, key=lambda h: h.degree())
            zeros = _solve_univariate(p)

            for zero in zeros:
                if not (zero in dom):
                    dom_zero = dom.algebraic_field(zero)
                else:
                    dom_zero = dom

                _solutions.add(((zero,) + values, dom_zero))

        solutions = _solutions
    return sorted((s for s, _ in solutions), key=default_sort_key)

