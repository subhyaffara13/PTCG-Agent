
def test_primenu():
    # error
    m = Symbol('m', integer=False)
    raises(TypeError, lambda: primenu(m))
    raises(TypeError, lambda: primenu(4.5))
    m = Symbol('m', positive=False)
    raises(ValueError, lambda: primenu(m))
    raises(ValueError, lambda: primenu(0))

    # special case
    p = Symbol('p', prime=True)
    assert primenu(p) == 1

    # property
    n = Symbol('n', integer=True, positive=True)
    assert primenu(n).is_integer is True
    assert primenu(n).is_nonnegative is True

    # Integer
    assert primenu(7*13) == 2
    assert primenu(2*17*19) == 3
    assert primenu(2**3 * 17 * 19**2) == 3
    A001221 = [0, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 2,
               1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 3, 1, 1, 2, 2, 2, 2]
    for n, val in enumerate(A001221, 1):
        assert primenu(n) == val

