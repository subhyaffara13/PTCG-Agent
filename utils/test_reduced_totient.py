
def test_reduced_totient():
    # error
    m = Symbol('m', integer=False)
    raises(TypeError, lambda: reduced_totient(m))
    raises(TypeError, lambda: reduced_totient(4.5))
    m = Symbol('m', positive=False)
    raises(ValueError, lambda: reduced_totient(m))
    raises(ValueError, lambda: reduced_totient(0))

    # special case
    p = Symbol('p', prime=True)
    assert reduced_totient(p) == p - 1

    # property
    n = Symbol('n', integer=True, positive=True)
    assert reduced_totient(n).is_integer is True
    assert reduced_totient(n).is_positive is True

    # Integer
    assert reduced_totient(7*13) == reduced_totient(factorint(7*13)) == 12
    assert reduced_totient(2*17*19) == reduced_totient(factorint(2*17*19)) == 144
    assert reduced_totient(2**2 * 11) == reduced_totient({2: 2, 11: 1}) == 10
    assert reduced_totient(2**3 * 17 * 19**2) == reduced_totient({2: 3, 17: 1, 19: 2}) == 2736
    A002322 = [1, 1, 2, 2, 4, 2, 6, 2, 6, 4, 10, 2, 12, 6, 4, 4, 16, 6,
               18, 4, 6, 10, 22, 2, 20, 12, 18, 6, 28, 4, 30, 8, 10, 16,
               12, 6, 36, 18, 12, 4, 40, 6, 42, 10, 12, 22, 46, 4, 42]
    for n, val in enumerate(A002322, 1):
        assert reduced_totient(n) == val

