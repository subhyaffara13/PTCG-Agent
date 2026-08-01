
def test_symbolic_Range():
    n = Symbol('n')
    raises(ValueError, lambda: Range(n)[0])
    raises(IndexError, lambda: Range(n, n)[0])
    raises(ValueError, lambda: Range(n, n+1)[0])
    raises(ValueError, lambda: Range(n).size)

    n = Symbol('n', integer=True)
    raises(ValueError, lambda: Range(n)[0])
    raises(IndexError, lambda: Range(n, n)[0])
    assert Range(n, n+1)[0] == n
    raises(ValueError, lambda: Range(n).size)
    assert Range(n, n+1).size == 1

    n = Symbol('n', integer=True, nonnegative=True)
    raises(ValueError, lambda: Range(n)[0])
    raises(IndexError, lambda: Range(n, n)[0])
    assert Range(n+1)[0] == 0
    assert Range(n, n+1)[0] == n
    assert Range(n).size == n
    assert Range(n+1).size == n+1
    assert Range(n, n+1).size == 1

    n = Symbol('n', integer=True, positive=True)
    assert Range(n)[0] == 0
    assert Range(n, n+1)[0] == n
    assert Range(n).size == n
    assert Range(n, n+1).size == 1

    m = Symbol('m', integer=True, positive=True)

    assert Range(n, n+m)[0] == n
    assert Range(n, n+m).size == m
    assert Range(n, n+1).size == 1
    assert Range(n, n+m, 2).size == floor(m/2)

    m = Symbol('m', integer=True, positive=True, even=True)
    assert Range(n, n+m, 2).size == m/2

