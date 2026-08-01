
def test_kronecker_symbol():
    # error
    m = Symbol('m', integer=False)
    raises(TypeError, lambda: kronecker_symbol(m, 3))
    raises(TypeError, lambda: kronecker_symbol(4.5, 3))
    raises(TypeError, lambda: kronecker_symbol(1, m))
    raises(TypeError, lambda: kronecker_symbol(1, 4.5))

    # special case
    p = Symbol('p', integer=True)
    assert kronecker_symbol(1, p) == 1
    assert kronecker_symbol(1, 1) == 1
    assert kronecker_symbol(0, 1) == 1

    # property
    n = Symbol('n')
    m = Symbol('m')
    assert kronecker_symbol(m, n).is_integer is True
    assert kronecker_symbol(m, n).is_prime is False

    # Integer
    for n in range(3, 10, 2):
        for a in range(-n, n):
            val = kronecker_symbol(a, n)
            assert val == jacobi_symbol(a, n)
            minus = kronecker_symbol(a, -n)
            if a < 0:
                assert -minus == val
            else:
                assert minus == val
            even = kronecker_symbol(a, 2 * n)
            if a % 2 == 0:
                assert even == 0
            elif a % 8 in [1, 7]:
                assert even == val
            else:
                assert -even == val
    assert kronecker_symbol(1, 0) == kronecker_symbol(-1, 0) == 1
    assert kronecker_symbol(0, 0) == 0

