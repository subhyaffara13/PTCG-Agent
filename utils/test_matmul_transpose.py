
def test_matmul_transpose():
    # https://github.com/sympy/sympy/issues/9503
    M = Matrix(2, 2, [1, 2 + I, 3, 4])
    a = Symbol('a')
    assert (MatMul(a, M).T).expand() == (a*Matrix([[1, 3],[2 + I, 4]])).expand()

