
def test_issue_17006():
    if not jax:
        skip("JAX not installed")

    M = MatrixSymbol("M", 2, 2)

    f = lambdify(M, M + Identity(2), 'jax')
    ma = jax.numpy.array([[1, 2], [3, 4]])
    mr = jax.numpy.array([[2, 2], [3, 5]])

    assert (f(ma) == mr).all()

    from sympy.core.symbol import symbols
    n = symbols('n', integer=True)
    N = MatrixSymbol("M", n, n)
    raises(NotImplementedError, lambda: lambdify(N, N + Identity(n), 'jax'))


def test_issue_17006():
    if not np:
        skip("NumPy not installed")

    M = MatrixSymbol("M", 2, 2)

    f = lambdify(M, M + Identity(2))
    ma = np.array([[1, 2], [3, 4]])
    mr = np.array([[2, 2], [3, 5]])

    assert (f(ma) == mr).all()

    from sympy.core.symbol import symbols
    n = symbols('n', integer=True)
    N = MatrixSymbol("M", n, n)
    raises(NotImplementedError, lambda: lambdify(N, N + Identity(n)))

