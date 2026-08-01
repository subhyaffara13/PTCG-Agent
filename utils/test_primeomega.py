
def test_primeomega():
    # error
    m = Symbol('m', integer=False)
    raises(TypeError, lambda: primeomega(m))
    raises(TypeError, lambda: primeomega(4.5))
    m = Symbol('m', positive=False)
    raises(ValueError, lambda: primeomega(m))
    raises(ValueError, lambda: primeomega(0))

    # special case
    p = Symbol('p', prime=True)
    assert primeomega(p) == 1

    # property
    n = Symbol('n', integer=True, positive=True)
    assert primeomega(n).is_integer is True
    assert primeomega(n).is_nonnegative is True

    # Integer
    assert primeomega(7*13) == 2
    assert primeomega(2*17*19) == 3
    assert primeomega(2**3 * 17 * 19**2) == 6
    A001222 = [0, 1, 1, 2, 1, 2, 1, 3, 2, 2, 1, 3, 1, 2, 2, 4, 1, 3,
               1, 3, 2, 2, 1, 4, 2, 2, 3, 3, 1, 3, 1, 5, 2, 2, 2, 4]
    for n, val in enumerate(A001222, 1):
        assert primeomega(n) == val

