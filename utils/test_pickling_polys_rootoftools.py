
def test_pickling_polys_rootoftools():
    from sympy.polys.rootoftools import CRootOf, RootSum

    x = Symbol('x')
    f = x**3 + x + 3

    for c in (CRootOf, CRootOf(f, 0)):
        check(c)

    for c in (RootSum, RootSum(f, exp)):
        check(c)

