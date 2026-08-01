
def test_divisor_sigma():
    # error
    m = Symbol('m', integer=False)
    raises(TypeError, lambda: divisor_sigma(m))
    raises(TypeError, lambda: divisor_sigma(4.5))
    raises(TypeError, lambda: divisor_sigma(1, m))
    raises(TypeError, lambda: divisor_sigma(1, 4.5))
    m = Symbol('m', positive=False)
    raises(ValueError, lambda: divisor_sigma(m))
    raises(ValueError, lambda: divisor_sigma(0))
    m = Symbol('m', negative=True)
    raises(ValueError, lambda: divisor_sigma(1, m))
    raises(ValueError, lambda: divisor_sigma(1, -1))

    # special case
    p = Symbol('p', prime=True)
    k = Symbol('k', integer=True)
    assert divisor_sigma(p, 1) == p + 1
    assert divisor_sigma(p, k) == p**k + 1

    # property
    n = Symbol('n', integer=True, positive=True)
    assert divisor_sigma(n).is_integer is True
    assert divisor_sigma(n).is_positive is True

    # symbolic
    k = Symbol('k', integer=True, zero=False)
    assert divisor_sigma(4, k) == 2**(2*k) + 2**k + 1
    assert divisor_sigma(6, k) == (2**k + 1) * (3**k + 1)

    # Integer
    assert divisor_sigma(23450) == 50592
    assert divisor_sigma(23450, 0) == 24
    assert divisor_sigma(23450, 1) == 50592
    assert divisor_sigma(23450, 2) == 730747500
    assert divisor_sigma(23450, 3) == 14666785333344

