
def test_CRootOf_real_roots():
    assert Poly(x**5 + x + 1).real_roots() == [rootof(x**3 - x**2 + 1, 0)]
    assert Poly(x**5 + x + 1).real_roots(radicals=False) == [rootof(
        x**3 - x**2 + 1, 0)]

    # https://github.com/sympy/sympy/issues/20902
    p = Poly(-3*x**4 - 10*x**3 - 12*x**2 - 6*x - 1, x, domain='ZZ')
    assert CRootOf.real_roots(p) == [S(-1), S(-1), S(-1), S(-1)/3]

    # with real algebraic coefficients
    assert Poly(x**3 + sqrt(2)*x**2 - 1, x, extension=True).real_roots() == [
        rootof(x**6 - 2*x**4 - 2*x**3 + 1, 0)
    ]
    assert Poly(x**5 + sqrt(2) * x**3 - 1, x, extension=True).real_roots() == [
        rootof(x**10 - 2*x**6 - 2*x**5 + 1, 0)
    ]
    r = rootof(y**5 + y**3 - 1, 0)
    assert Poly(x**5 + r*x - 1, x, extension=True).real_roots() ==\
    [
        rootof(x**25 - 5*x**20 + x**17 + 10*x**15 - 3*x**12 -
               10*x**10 + 3*x**7 + 6*x**5 - x**2 - 1, 0)
    ]
    # roots with multiplicity
    assert Poly((x-1) * (x-sqrt(2))**2, x, extension=True).real_roots() ==\
    [
        S(1), sqrt(2), sqrt(2)
    ]

