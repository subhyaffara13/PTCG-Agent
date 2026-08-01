
def test_RecursiveSeq():
    y = Function('y')
    n = Symbol('n')
    fib = RecursiveSeq(y(n - 1) + y(n - 2), y(n), n, [0, 1])
    assert fib.coeff(3) == 2

