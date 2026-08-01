
def _make_converter(K):
    """Construct the converter to convert back to Expr"""
    # Precompute the effect of converting to SymPy and expanding expressions
    # like (sqrt(2) + sqrt(3))**2. Asking Expr to do the expansion on every
    # conversion from K to Expr is slow. Here we compute the expansions for
    # each power of the generator and collect together the resulting algebraic
    # terms and the rational coefficients into a matrix.

    ext = K.ext.as_expr()
    todom = K.dom.from_sympy
    toexpr = K.dom.to_sympy

    if not ext.is_Add:
        powers = [ext**n for n in range(K.mod.degree())]
    else:
        # primitive_element generates a QQ-linear combination of lower degree
        # algebraic numbers to generate the higher degree extension e.g.
        # QQ<sqrt(2)+sqrt(3)> That means that we end up having high powers of low
        # degree algebraic numbers that can be reduced. Here we will use the
        # minimal polynomials of the algebraic numbers to reduce those powers
        # before converting to Expr.
        from sympy.polys.numberfields.minpoly import minpoly

        # Decompose ext as a linear combination of gens and make a symbol for
        # each gen.
        gens, coeffs = zip(*ext.as_coefficients_dict().items())
        syms = symbols(f'a:{len(gens)}', cls=Dummy)
        sym2gen = dict(zip(syms, gens))

        # Make a polynomial ring that can express ext and minpolys of all gens
        # in terms of syms.
        R = K.dom[syms]
        monoms = [R.ring.monomial_basis(i) for i in range(R.ngens)]
        ext_dict = {m: todom(c) for m, c in zip(monoms, coeffs)}
        ext_poly = R.ring.from_dict(ext_dict)
        minpolys = [R.from_sympy(minpoly(g, s)) for s, g in sym2gen.items()]

        # Compute all powers of ext_poly reduced modulo minpolys
        powers = [R.one, ext_poly]
        for n in range(2, K.mod.degree()):
            ext_poly_n = (powers[-1] * ext_poly).rem(minpolys)
            powers.append(ext_poly_n)

        # Convert the powers back to Expr. This will recombine some things like
        # sqrt(2)*sqrt(3) -> sqrt(6).
        powers = [p.as_expr().xreplace(sym2gen) for p in powers]

    # This also expands some rational powers
    powers = [p.expand() for p in powers]

    # Collect the rational coefficients and algebraic Expr that can
    # map the ANP coefficients into an expanded SymPy expression
    terms = [dict(t.as_coeff_Mul()[::-1] for t in Add.make_args(p)) for p in powers]
    algebraics = set().union(*terms)
    matrix = [[todom(t.get(a, S.Zero)) for t in terms] for a in algebraics]

    # Create a function to do the conversion efficiently:

    def converter(a):
        """Convert a to Expr using converter"""
        ai = a.to_list()[::-1]
        coeffs_dom = [sum(mij*aj for mij, aj in zip(mi, ai)) for mi in matrix]
        coeffs_sympy = [toexpr(c) for c in coeffs_dom]
        res = Add(*(Mul(c, a) for c, a in zip(coeffs_sympy, algebraics)))
        return res

    return converter

