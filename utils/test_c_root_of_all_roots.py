
def test_CRootOf_all_roots():
    assert Poly(x**5 + x + 1).all_roots() == [
        rootof(x**3 - x**2 + 1, 0),
        Rational(-1, 2) - sqrt(3)*I/2,
        Rational(-1, 2) + sqrt(3)*I/2,
        rootof(x**3 - x**2 + 1, 1),
        rootof(x**3 - x**2 + 1, 2),
    ]

    assert Poly(x**5 + x + 1).all_roots(radicals=False) == [
        rootof(x**3 - x**2 + 1, 0),
        rootof(x**2 + x + 1, 0, radicals=False),
        rootof(x**2 + x + 1, 1, radicals=False),
        rootof(x**3 - x**2 + 1, 1),
        rootof(x**3 - x**2 + 1, 2),
    ]

    # with real algebraic coefficients
    assert Poly(x**3 + sqrt(2)*x**2 - 1, x, extension=True).all_roots() ==\
    [
        rootof(x**6 - 2*x**4 - 2*x**3 + 1, 0),
        rootof(x**6 - 2*x**4 - 2*x**3 + 1, 2),
        rootof(x**6 - 2*x**4 - 2*x**3 + 1, 3)
    ]
    # roots with multiplicity
    assert Poly((x-1) * (x-sqrt(2))**2 * (x-I) * (x+I), x, extension=True).all_roots() ==\
    [
        S(1), sqrt(2), sqrt(2), -I, I
    ]

    # imaginary algebraic coeffs (gaussian domain)
    assert Poly(x**2 - I/2, x, extension=True).all_roots() ==\
    [
        S(1)/2 + I/2,
        -S(1)/2 - I/2
    ]

