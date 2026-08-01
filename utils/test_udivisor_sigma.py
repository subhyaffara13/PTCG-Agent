
def test_udivisor_sigma():
    # error
    m = Symbol('m', integer=False)
    raises(TypeError, lambda: udivisor_sigma(m))
    raises(TypeError, lambda: udivisor_sigma(4.5))
    raises(TypeError, lambda: udivisor_sigma(1, m))
    raises(TypeError, lambda: udivisor_sigma(1, 4.5))
    m = Symbol('m', positive=False)
    raises(ValueError, lambda: udivisor_sigma(m))
    raises(ValueError, lambda: udivisor_sigma(0))
    m = Symbol('m', negative=True)
    raises(ValueError, lambda: udivisor_sigma(1, m))
    raises(ValueError, lambda: udivisor_sigma(1, -1))

    # special case
    p = Symbol('p', prime=True)
    k = Symbol('k', integer=True)
    assert udivisor_sigma(p, 1) == p + 1
    assert udivisor_sigma(p, k) == p**k + 1

    # property
    n = Symbol('n', integer=True, positive=True)
    assert udivisor_sigma(n).is_integer is True
    assert udivisor_sigma(n).is_positive is True

    # Integer
    A034444 = [1, 2, 2, 2, 2, 4, 2, 2, 2, 4, 2, 4, 2, 4, 4, 2, 2, 4, 2, 4,
               4, 4, 2, 4, 2, 4, 2, 4, 2, 8, 2, 2, 4, 4, 4, 4, 2, 4, 4, 4,
               2, 8, 2, 4, 4, 4, 2, 4, 2, 4, 4, 4, 2, 4, 4, 4, 4, 4, 2, 8]
    for n, val in enumerate(A034444, 1):
        assert udivisor_sigma(n, 0) == val
    A034448 = [1, 3, 4, 5, 6, 12, 8, 9, 10, 18, 12, 20, 14, 24, 24, 17, 18,
               30, 20, 30, 32, 36, 24, 36, 26, 42, 28, 40, 30, 72, 32, 33,
               48, 54, 48, 50, 38, 60, 56, 54, 42, 96, 44, 60, 60, 72, 48]
    for n, val in enumerate(A034448, 1):
        assert udivisor_sigma(n, 1) == val
    A034676 = [1, 5, 10, 17, 26, 50, 50, 65, 82, 130, 122, 170, 170, 250,
               260, 257, 290, 410, 362, 442, 500, 610, 530, 650, 626, 850,
               730, 850, 842, 1300, 962, 1025, 1220, 1450, 1300, 1394, 1370]
    for n, val in enumerate(A034676, 1):
        assert udivisor_sigma(n, 2) == val

