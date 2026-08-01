
def test_jacobi_symbol():
    # error
    m = Symbol('m', integer=False)
    raises(TypeError, lambda: jacobi_symbol(m, 3))
    raises(TypeError, lambda: jacobi_symbol(4.5, 3))
    raises(TypeError, lambda: jacobi_symbol(1, m))
    raises(TypeError, lambda: jacobi_symbol(1, 4.5))
    m = Symbol('m', positive=False)
    raises(ValueError, lambda: jacobi_symbol(1, m))
    raises(ValueError, lambda: jacobi_symbol(1, -6))
    m = Symbol('m', odd=False)
    raises(ValueError, lambda: jacobi_symbol(1, m))
    raises(ValueError, lambda: jacobi_symbol(1, 2))

    # special case
    p = Symbol('p', integer=True)
    k = Symbol('k', integer=True)
    assert jacobi_symbol(p*k, p) == 0
    assert jacobi_symbol(1, p) == 1
    assert jacobi_symbol(1, 1) == 1
    assert jacobi_symbol(0, 1) == 1

    # property
    n = Symbol('n')
    m = Symbol('m')
    assert jacobi_symbol(m, n).is_integer is True
    assert jacobi_symbol(m, n).is_prime is False

    # Integer
    assert jacobi_symbol(25, 41) == 1
    assert jacobi_symbol(-23, 83) == -1
    assert jacobi_symbol(3, 9) == 0
    assert jacobi_symbol(42, 97) == -1
    assert jacobi_symbol(3, 5) == -1
    assert jacobi_symbol(7, 9) == 1
    assert jacobi_symbol(0, 3) == 0
    assert jacobi_symbol(0, 1) == 1
    assert jacobi_symbol(2, 1) == 1
    assert jacobi_symbol(1, 3) == 1

