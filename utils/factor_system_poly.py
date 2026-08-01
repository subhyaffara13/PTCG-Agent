
def factor_system_poly(polys: list[Poly]) -> list[list[Poly]]:
    """
    Factors a system of polynomial equations into irreducible subsystems

    Core implementation that works directly with Poly instances.

    Parameters
    ==========

    polys : list[Poly]
        A list of Poly instances to be factored.

    Returns
    =======

    list[list[Poly]]
        A list of lists of polynomials, where each sublist represents
        an irreducible component of the solution. Includes both
        generic and degenerate cases.

    Examples
    ========

    >>> from sympy import symbols, Poly, ZZ
    >>> from sympy.solvers.polysys import factor_system_poly
    >>> a, b, c, x = symbols('a b c x')
    >>> p1 = Poly((a - 1)*(x - 2), x, domain=ZZ[a,b,c])
    >>> p2 = Poly((b - 3)*(x - 2), x, domain=ZZ[a,b,c])
    >>> p3 = Poly(c, x, domain=ZZ[a,b,c])

    The equation to be solved for x is ``x - 2 = 0`` provided either
    of the two conditions on the parameters ``a`` and ``b`` is nonzero
    and the constant parameter ``c`` should be zero.

    >>> sys1, sys2 = factor_system_poly([p1, p2, p3])
    >>> sys1
    [Poly(x - 2, x, domain='ZZ[a,b,c]'),
     Poly(c, x, domain='ZZ[a,b,c]')]
    >>> sys2
    [Poly(a - 1, x, domain='ZZ[a,b,c]'),
     Poly(b - 3, x, domain='ZZ[a,b,c]'),
     Poly(c, x, domain='ZZ[a,b,c]')]

     An empty list [] when returned means no solution exists.
     Whereas a list containing an empty list [[]] means any value is a solution.

    See Also
    ========

    factor_system : Returns only generic solutions
    factor_system_bool : Returns a Boolean combination representing the solutions
    factor_system_cond : Returns both generic and degenerate solutions
    sympy.polys.polytools.factor : Factors a polynomial into irreducible factors
                                   over the rational numbers
    """
    if not all(isinstance(poly, Poly) for poly in polys):
        raise TypeError("polys should be a list of Poly instances")
    if not polys:
        return [[]]

    base_domain = polys[0].domain
    base_gens = polys[0].gens
    if not all(poly.domain == base_domain and poly.gens == base_gens for poly in polys[1:]):
        raise DomainError("All polynomials must have the same domain and generators")

    factor_sets = []
    for poly in polys:
        constant, factors_mult = poly.factor_list()

        if constant.is_zero is True:
            continue
        elif constant.is_zero is False:
            if not factors_mult:
                return []
            factor_sets.append([f for f, _ in factors_mult])
        else:
            constant = sqf_part(factor_terms(constant).as_coeff_Mul()[1])
            constp = Poly(constant, base_gens, domain=base_domain)
            factors = [f for f, _ in factors_mult]
            factors.append(constp)
            factor_sets.append(factors)

    if not factor_sets:
        return [[]]

    result = _factor_sets(factor_sets)
    return _sort_systems(result)

