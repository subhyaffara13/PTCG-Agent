
def test_fraction():
    x, y, z = map(Symbol, 'xyz')
    A = Symbol('A', commutative=False)

    assert fraction(S.Half) == (1, 2)

    assert fraction(x) == (x, 1)
    assert fraction(1/x) == (1, x)
    assert fraction(x/y) == (x, y)
    assert fraction(x/2) == (x, 2)

    assert fraction(x*y/z) == (x*y, z)
    assert fraction(x/(y*z)) == (x, y*z)

    assert fraction(1/y**2) == (1, y**2)
    assert fraction(x/y**2) == (x, y**2)

    assert fraction((x**2 + 1)/y) == (x**2 + 1, y)
    assert fraction(x*(y + 1)/y**7) == (x*(y + 1), y**7)

    assert fraction(exp(-x), exact=True) == (exp(-x), 1)
    assert fraction((1/(x + y))/2, exact=True) == (1, Mul(2,(x + y), evaluate=False))

    assert fraction(x*A/y) == (x*A, y)
    assert fraction(x*A**-1/y) == (x*A**-1, y)

    n = symbols('n', negative=True)
    assert fraction(exp(n)) == (1, exp(-n))
    assert fraction(exp(-n)) == (exp(-n), 1)

    p = symbols('p', positive=True)
    assert fraction(exp(-p)*log(p), exact=True) == (exp(-p)*log(p), 1)

    m = Mul(1, 1, S.Half, evaluate=False)
    assert fraction(m) == (1, 2)
    assert fraction(m, exact=True) == (Mul(1, 1, evaluate=False), 2)

    m = Mul(1, 1, S.Half, S.Half, Pow(1, -1, evaluate=False), evaluate=False)
    assert fraction(m) == (1, 4)
    assert fraction(m, exact=True) == \
            (Mul(1, 1, evaluate=False), Mul(2, 2, 1, evaluate=False))

