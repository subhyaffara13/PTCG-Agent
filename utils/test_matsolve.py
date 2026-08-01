
def test_matsolve():
    if not np:
        skip("NumPy not installed")

    M = MatrixSymbol("M", 3, 3)
    x = MatrixSymbol("x", 3, 1)

    expr = M**(-1) * x + x
    matsolve_expr = MatrixSolve(M, x) + x

    f = lambdify((M, x), expr)
    f_matsolve = lambdify((M, x), matsolve_expr)

    m0 = np.array([[1, 2, 3], [3, 2, 5], [5, 6, 7]])
    assert np.linalg.matrix_rank(m0) == 3

    x0 = np.array([3, 4, 5])

    assert np.allclose(f_matsolve(m0, x0), f(m0, x0))


def test_matsolve():
    n = Symbol('n', integer=True)
    A = MatrixSymbol('A', n, n)
    x = MatrixSymbol('x', n, 1)

    with assuming(Q.fullrank(A)):
        assert optimize(A**(-1) * x, [matinv_opt]) == MatrixSolve(A, x)
        assert optimize(A**(-1) * x + x, [matinv_opt]) == MatrixSolve(A, x) + x

