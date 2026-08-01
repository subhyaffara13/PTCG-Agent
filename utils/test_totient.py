
def test_totient():
    # error
    m = Symbol('m', integer=False)
    raises(TypeError, lambda: totient(m))
    raises(TypeError, lambda: totient(4.5))
    m = Symbol('m', positive=False)
    raises(ValueError, lambda: totient(m))
    raises(ValueError, lambda: totient(0))

    # special case
    p = Symbol('p', prime=True)
    assert totient(p) == p - 1

    # property
    n = Symbol('n', integer=True, positive=True)
    assert totient(n).is_integer is True
    assert totient(n).is_positive is True

    # Integer
    assert totient(7*13) == totient(factorint(7*13)) == (7-1)*(13-1)
    assert totient(2*17*19) == totient(factorint(2*17*19)) == (17-1)*(19-1)
    assert totient(2**3 * 17 * 19**2) == totient({2: 3, 17: 1, 19: 2}) == 2**2 * (17-1) * 19*(19-1)
    A000010 = [1, 1, 2, 2, 4, 2, 6, 4, 6, 4, 10, 4, 12, 6, 8, 8, 16,
               6, 18, 8, 12, 10, 22, 8, 20, 12, 18, 12, 28, 8, 30, 16,
               20, 16, 24, 12, 36, 18, 24, 16, 40, 12, 42, 20, 24, 22]
    for n, val in enumerate(A000010, 1):
        assert totient(n) == val

