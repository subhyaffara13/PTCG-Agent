
def test_pickling_polys_polytools():
    from sympy.polys.polytools import PurePoly
    # from sympy.polys.polytools import GroebnerBasis
    x = Symbol('x')

    for c in (Poly, Poly(x, x)):
        check(c)

    for c in (PurePoly, PurePoly(x)):
        check(c)

