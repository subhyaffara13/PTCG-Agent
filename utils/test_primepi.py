
def test_primepi():
    # error
    z = Symbol('z', real=False)
    raises(TypeError, lambda: primepi(z))
    raises(TypeError, lambda: primepi(I))

    # property
    n = Symbol('n', integer=True, positive=True)
    assert primepi(n).is_integer is True
    assert primepi(n).is_nonnegative is True

    # infinity
    assert primepi(oo) == oo
    assert primepi(-oo) == 0

    # symbol
    x = Symbol('x')
    assert isinstance(primepi(x), primepi)

    # Integer
    assert primepi(0) == 0
    A000720 = [0, 1, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 6, 6, 6, 6, 7, 7, 8,
               8, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 11, 11, 11, 11, 11, 11,
               12, 12, 12, 12, 13, 13, 14, 14, 14, 14, 15, 15, 15, 15]
    for n, val in enumerate(A000720, 1):
        assert primepi(n) == primepi(n + 0.5) == val

