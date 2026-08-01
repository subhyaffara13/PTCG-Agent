
def test_bell():
    assert [bell(n) for n in range(8)] == [1, 1, 2, 5, 15, 52, 203, 877]

    assert bell(0, x) == 1
    assert bell(1, x) == x
    assert bell(2, x) == x**2 + x
    assert bell(5, x) == x**5 + 10*x**4 + 25*x**3 + 15*x**2 + x
    assert bell(oo) is S.Infinity
    raises(ValueError, lambda: bell(oo, x))

    raises(ValueError, lambda: bell(-1))
    raises(ValueError, lambda: bell(S.Half))

    X = symbols('x:6')
    # X = (x0, x1, .. x5)
    # at the same time: X[1] = x1, X[2] = x2 for standard readablity.
    # but we must supply zero-based indexed object X[1:] = (x1, .. x5)

    assert bell(6, 2, X[1:]) == 6*X[5]*X[1] + 15*X[4]*X[2] + 10*X[3]**2
    assert bell(
        6, 3, X[1:]) == 15*X[4]*X[1]**2 + 60*X[3]*X[2]*X[1] + 15*X[2]**3

    X = (1, 10, 100, 1000, 10000)
    assert bell(6, 2, X) == (6 + 15 + 10)*10000

    X = (1, 2, 3, 3, 5)
    assert bell(6, 2, X) == 6*5 + 15*3*2 + 10*3**2

    X = (1, 2, 3, 5)
    assert bell(6, 3, X) == 15*5 + 60*3*2 + 15*2**3

    # Dobinski's formula
    n = Symbol('n', integer=True, nonnegative=True)
    # For large numbers, this is too slow
    # For nonintegers, there are significant precision errors
    for i in [0, 2, 3, 7, 13, 42, 55]:
        # Running without the cache this is either very slow or goes into an
        # infinite loop.
        assert bell(i).evalf() == bell(n).rewrite(Sum).evalf(subs={n: i})

    m = Symbol("m")
    assert bell(m).rewrite(Sum) == bell(m)
    assert bell(n, m).rewrite(Sum) == bell(n, m)
    # issue 9184
    n = Dummy('n')
    assert bell(n).limit(n, S.Infinity) is S.Infinity

