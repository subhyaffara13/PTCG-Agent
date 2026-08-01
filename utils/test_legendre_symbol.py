
def test_legendre_symbol():
    # error
    m = Symbol('m', integer=False)
    raises(TypeError, lambda: legendre_symbol(m, 3))
    raises(TypeError, lambda: legendre_symbol(4.5, 3))
    raises(TypeError, lambda: legendre_symbol(1, m))
    raises(TypeError, lambda: legendre_symbol(1, 4.5))
    m = Symbol('m', prime=False)
    raises(ValueError, lambda: legendre_symbol(1, m))
    raises(ValueError, lambda: legendre_symbol(1, 6))
    m = Symbol('m', odd=False)
    raises(ValueError, lambda: legendre_symbol(1, m))
    raises(ValueError, lambda: legendre_symbol(1, 2))

    # special case
    p = Symbol('p', prime=True)
    k = Symbol('k', integer=True)
    assert legendre_symbol(p*k, p) == 0
    assert legendre_symbol(1, p) == 1

    # property
    n = Symbol('n')
    m = Symbol('m')
    assert legendre_symbol(m, n).is_integer is True
    assert legendre_symbol(m, n).is_prime is False

    # Integer
    assert legendre_symbol(5, 11) == 1
    assert legendre_symbol(25, 41) == 1
    assert legendre_symbol(67, 101) == -1
    assert legendre_symbol(0, 13) == 0
    assert legendre_symbol(9, 3) == 0

