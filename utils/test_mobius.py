
def test_mobius():
    # error
    m = Symbol('m', integer=False)
    raises(TypeError, lambda: mobius(m))
    raises(TypeError, lambda: mobius(4.5))
    m = Symbol('m', positive=False)
    raises(ValueError, lambda: mobius(m))
    raises(ValueError, lambda: mobius(-3))

    # special case
    p = Symbol('p', prime=True)
    assert mobius(p) == -1

    # property
    n = Symbol('n', integer=True, positive=True)
    assert mobius(n).is_integer is True
    assert mobius(n).is_prime is False

    # symbolic
    n = Symbol('n', integer=True, positive=True)
    k = Symbol('k', integer=True, positive=True)
    assert mobius(n**2) == 0
    assert mobius(4*n) == 0
    assert isinstance(mobius(n**k), mobius)
    assert mobius(n**(k+1)) == 0
    assert isinstance(mobius(3**k), mobius)
    assert mobius(3**(k+1)) == 0
    m = Symbol('m')
    assert isinstance(mobius(4*m), mobius)

    # Integer
    assert mobius(13*7) == 1
    assert mobius(1) == 1
    assert mobius(13*7*5) == -1
    assert mobius(13**2) == 0
    A008683 = [1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0, -1, 1, 1, 0, -1, 0,
               -1, 0, 1, 1, -1, 0, 0, 1, 0, 0, -1, -1, -1, 0, 1, 1, 1, 0, -1,
               1, 1, 0, -1, -1, -1, 0, 0, 1, -1, 0, 0, 0, 1, 0, -1, 0, 1, 0]
    for n, val in enumerate(A008683, 1):
        assert mobius(n) == val

