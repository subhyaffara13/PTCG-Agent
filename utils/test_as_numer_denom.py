
def test_as_numer_denom():
    n = symbols('n', negative=True)
    assert exp(x).as_numer_denom() == (exp(x), 1)
    assert exp(-x).as_numer_denom() == (1, exp(x))
    assert exp(-2*x).as_numer_denom() == (1, exp(2*x))
    assert exp(-2).as_numer_denom() == (1, exp(2))
    assert exp(n).as_numer_denom() == (1, exp(-n))
    assert exp(-n).as_numer_denom() == (exp(-n), 1)
    assert exp(-I*x).as_numer_denom() == (1, exp(I*x))
    assert exp(-I*n).as_numer_denom() == (1, exp(I*n))
    assert exp(-n).as_numer_denom() == (exp(-n), 1)
    # Check noncommutativity
    a = symbols('a', commutative=False)
    assert exp(-a).as_numer_denom() == (exp(-a), 1)


def test_as_numer_denom():
    a, b, c = symbols('a, b, c')

    assert nan.as_numer_denom() == (nan, 1)
    assert oo.as_numer_denom() == (oo, 1)
    assert (-oo).as_numer_denom() == (-oo, 1)
    assert zoo.as_numer_denom() == (zoo, 1)
    assert (-zoo).as_numer_denom() == (zoo, 1)

    assert x.as_numer_denom() == (x, 1)
    assert (1/x).as_numer_denom() == (1, x)
    assert (x/y).as_numer_denom() == (x, y)
    assert (x/2).as_numer_denom() == (x, 2)
    assert (x*y/z).as_numer_denom() == (x*y, z)
    assert (x/(y*z)).as_numer_denom() == (x, y*z)
    assert S.Half.as_numer_denom() == (1, 2)
    assert (1/y**2).as_numer_denom() == (1, y**2)
    assert (x/y**2).as_numer_denom() == (x, y**2)
    assert ((x**2 + 1)/y).as_numer_denom() == (x**2 + 1, y)
    assert (x*(y + 1)/y**7).as_numer_denom() == (x*(y + 1), y**7)
    assert (x**-2).as_numer_denom() == (1, x**2)
    assert (a/x + b/2/x + c/3/x).as_numer_denom() == \
        (6*a + 3*b + 2*c, 6*x)
    assert (a/x + b/2/x + c/3/y).as_numer_denom() == \
        (2*c*x + y*(6*a + 3*b), 6*x*y)
    assert (a/x + b/2/x + c/.5/x).as_numer_denom() == \
        (2*a + b + 4.0*c, 2*x)
    # this should take no more than a few seconds
    assert int(log(Add(*[Dummy()/i/x for i in range(1, 705)]
                       ).as_numer_denom()[1]/x).n(4)) == 705
    for i in [S.Infinity, S.NegativeInfinity, S.ComplexInfinity]:
        assert (i + x/3).as_numer_denom() == \
            (x + i, 3)
    assert (S.Infinity + x/3 + y/4).as_numer_denom() == \
        (4*x + 3*y + S.Infinity, 12)
    assert (oo*x + zoo*y).as_numer_denom() == \
        (zoo*y + oo*x, 1)

    A, B, C = symbols('A,B,C', commutative=False)

    assert (A*B*C**-1).as_numer_denom() == (A*B*C**-1, 1)
    assert (A*B*C**-1/x).as_numer_denom() == (A*B*C**-1, x)
    assert (C**-1*A*B).as_numer_denom() == (C**-1*A*B, 1)
    assert (C**-1*A*B/x).as_numer_denom() == (C**-1*A*B, x)
    assert ((A*B*C)**-1).as_numer_denom() == ((A*B*C)**-1, 1)
    assert ((A*B*C)**-1/x).as_numer_denom() == ((A*B*C)**-1, x)

    # the following morphs from Add to Mul during processing
    assert Add(0, (x + y)/z/-2, evaluate=False).as_numer_denom(
        ) == (-x - y, 2*z)

