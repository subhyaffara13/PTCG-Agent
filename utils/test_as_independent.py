
def test_as_independent():
    assert S.Zero.as_independent(x, as_Add=True) == (0, 0)
    assert S.Zero.as_independent(x, as_Add=False) == (0, 0)
    assert (2*x*sin(x) + y + x).as_independent(x) == (y, x + 2*x*sin(x))
    assert (2*x*sin(x) + y + x).as_independent(y) == (x + 2*x*sin(x), y)

    assert (2*x*sin(x) + y + x).as_independent(x, y) == (0, y + x + 2*x*sin(x))

    assert (x*sin(x)*cos(y)).as_independent(x) == (cos(y), x*sin(x))
    assert (x*sin(x)*cos(y)).as_independent(y) == (x*sin(x), cos(y))

    assert (x*sin(x)*cos(y)).as_independent(x, y) == (1, x*sin(x)*cos(y))

    assert (sin(x)).as_independent(x) == (1, sin(x))
    assert (sin(x)).as_independent(y) == (sin(x), 1)

    assert (2*sin(x)).as_independent(x) == (2, sin(x))
    assert (2*sin(x)).as_independent(y) == (2*sin(x), 1)

    # issue 4903 = 1766b
    n1, n2, n3 = symbols('n1 n2 n3', commutative=False)
    assert (n1 + n1*n2).as_independent(n2) == (n1, n1*n2)
    assert (n2*n1 + n1*n2).as_independent(n2) == (0, n1*n2 + n2*n1)
    assert (n1*n2*n1).as_independent(n2) == (n1, n2*n1)
    assert (n1*n2*n1).as_independent(n1) == (1, n1*n2*n1)

    assert (3*x).as_independent(x, as_Add=True) == (0, 3*x)
    assert (3*x).as_independent(x, as_Add=False) == (3, x)
    assert (3 + x).as_independent(x, as_Add=True) == (3, x)
    assert (3 + x).as_independent(x, as_Add=False) == (1, 3 + x)

    # issue 5479
    assert (3*x).as_independent(Symbol) == (3, x)

    # issue 5648
    assert (n1*x*y).as_independent(x) == (n1*y, x)
    assert ((x + n1)*(x - y)).as_independent(x) == (1, (x + n1)*(x - y))
    assert ((x + n1)*(x - y)).as_independent(y) == (x + n1, x - y)
    assert (DiracDelta(x - n1)*DiracDelta(x - y)).as_independent(x) \
        == (1, DiracDelta(x - n1)*DiracDelta(x - y))
    assert (x*y*n1*n2*n3).as_independent(n2) == (x*y*n1, n2*n3)
    assert (x*y*n1*n2*n3).as_independent(n1) == (x*y, n1*n2*n3)
    assert (x*y*n1*n2*n3).as_independent(n3) == (x*y*n1*n2, n3)
    assert (DiracDelta(x - n1)*DiracDelta(y - n1)*DiracDelta(x - n2)).as_independent(y) == \
           (DiracDelta(x - n1)*DiracDelta(x - n2), DiracDelta(y - n1))

    # issue 5784
    assert (x + Integral(x, (x, 1, 2))).as_independent(x, strict=True) == \
           (Integral(x, (x, 1, 2)), x)

    eq = Add(x, -x, 2, -3, evaluate=False)
    assert eq.as_independent(x) == (-1, Add(x, -x, evaluate=False))
    eq = Mul(x, 1/x, 2, -3, evaluate=False)
    assert eq.as_independent(x) == (-6, Mul(x, 1/x, evaluate=False))

    assert (x*y).as_independent(z, as_Add=True) == (x*y, 0)

