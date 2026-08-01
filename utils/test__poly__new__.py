
def test_Poly__new__():
    raises(GeneratorsError, lambda: Poly(x + 1, x, x))

    raises(GeneratorsError, lambda: Poly(x + y, x, y, domain=ZZ[x]))
    raises(GeneratorsError, lambda: Poly(x + y, x, y, domain=ZZ[y]))

    raises(OptionError, lambda: Poly(x, x, symmetric=True))
    raises(OptionError, lambda: Poly(x + 2, x, modulus=3, domain=QQ))

    raises(OptionError, lambda: Poly(x + 2, x, domain=ZZ, gaussian=True))
    raises(OptionError, lambda: Poly(x + 2, x, modulus=3, gaussian=True))

    raises(OptionError, lambda: Poly(x + 2, x, domain=ZZ, extension=[sqrt(3)]))
    raises(OptionError, lambda: Poly(x + 2, x, modulus=3, extension=[sqrt(3)]))

    raises(OptionError, lambda: Poly(x + 2, x, domain=ZZ, extension=True))
    raises(OptionError, lambda: Poly(x + 2, x, modulus=3, extension=True))

    raises(OptionError, lambda: Poly(x + 2, x, domain=ZZ, greedy=True))
    raises(OptionError, lambda: Poly(x + 2, x, domain=QQ, field=True))

    raises(OptionError, lambda: Poly(x + 2, x, domain=ZZ, greedy=False))
    raises(OptionError, lambda: Poly(x + 2, x, domain=QQ, field=False))

    raises(NotImplementedError, lambda: Poly(x + 1, x, modulus=3, order='grlex'))
    raises(NotImplementedError, lambda: Poly(x + 1, x, order='grlex'))

    raises(GeneratorsNeeded, lambda: Poly({1: 2, 0: 1}))
    raises(GeneratorsNeeded, lambda: Poly([2, 1]))
    raises(GeneratorsNeeded, lambda: Poly((2, 1)))

    raises(GeneratorsNeeded, lambda: Poly(1))

    assert Poly('x-x') == Poly(0, x)

    f = a*x**2 + b*x + c

    assert Poly({2: a, 1: b, 0: c}, x) == f
    assert Poly(iter([a, b, c]), x) == f
    assert Poly([a, b, c], x) == f
    assert Poly((a, b, c), x) == f

    f = Poly({}, x, y, z)

    assert f.gens == (x, y, z) and f.as_expr() == 0

    assert Poly(Poly(a*x + b*y, x, y), x) == Poly(a*x + b*y, x)

    assert Poly(3*x**2 + 2*x + 1, domain='ZZ').all_coeffs() == [3, 2, 1]
    assert Poly(3*x**2 + 2*x + 1, domain='QQ').all_coeffs() == [3, 2, 1]
    assert Poly(3*x**2 + 2*x + 1, domain='RR').all_coeffs() == [3.0, 2.0, 1.0]

    raises(CoercionFailed, lambda: Poly(3*x**2/5 + x*Rational(2, 5) + 1, domain='ZZ'))
    assert Poly(
        3*x**2/5 + x*Rational(2, 5) + 1, domain='QQ').all_coeffs() == [Rational(3, 5), Rational(2, 5), 1]
    assert _epsilon_eq(
        Poly(3*x**2/5 + x*Rational(2, 5) + 1, domain='RR').all_coeffs(), [0.6, 0.4, 1.0])

    assert Poly(3.0*x**2 + 2.0*x + 1, domain='ZZ').all_coeffs() == [3, 2, 1]
    assert Poly(3.0*x**2 + 2.0*x + 1, domain='QQ').all_coeffs() == [3, 2, 1]
    assert Poly(
        3.0*x**2 + 2.0*x + 1, domain='RR').all_coeffs() == [3.0, 2.0, 1.0]

    raises(CoercionFailed, lambda: Poly(3.1*x**2 + 2.1*x + 1, domain='ZZ'))
    assert Poly(3.1*x**2 + 2.1*x + 1, domain='QQ').all_coeffs() == [Rational(31, 10), Rational(21, 10), 1]
    assert Poly(3.1*x**2 + 2.1*x + 1, domain='RR').all_coeffs() == [3.1, 2.1, 1.0]

    assert Poly({(2, 1): 1, (1, 2): 2, (1, 1): 3}, x, y) == \
        Poly(x**2*y + 2*x*y**2 + 3*x*y, x, y)

    assert Poly(x**2 + 1, extension=I).get_domain() == QQ.algebraic_field(I)

    f = 3*x**5 - x**4 + x**3 - x** 2 + 65538

    assert Poly(f, x, modulus=65537, symmetric=True) == \
        Poly(3*x**5 - x**4 + x**3 - x** 2 + 1, x, modulus=65537,
             symmetric=True)
    assert Poly(f, x, modulus=65537, symmetric=False) == \
        Poly(3*x**5 + 65536*x**4 + x**3 + 65536*x** 2 + 1, x,
             modulus=65537, symmetric=False)

    N = 10**100
    assert Poly(-1, x, modulus=N, symmetric=False).as_expr() == N - 1

    assert isinstance(Poly(x**2 + x + 1.0).get_domain(), RealField)
    assert isinstance(Poly(x**2 + x + I + 1.0).get_domain(), ComplexField)

