
def test_pickling_polys_monomials():
    from sympy.polys.monomials import MonomialOps, Monomial
    x, y, z = symbols("x,y,z")

    for c in (MonomialOps, MonomialOps(3)):
        check(c)

    for c in (Monomial, Monomial((1, 2, 3), (x, y, z))):
        check(c)

