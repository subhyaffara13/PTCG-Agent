
def test_jax_matsolve():
    if not jax:
        skip("JAX not installed")

    M = MatrixSymbol("M", 3, 3)
    x = MatrixSymbol("x", 3, 1)

    expr = M**(-1) * x + x
    matsolve_expr = MatrixSolve(M, x) + x

    f = lambdify((M, x), expr, 'jax')
    f_matsolve = lambdify((M, x), matsolve_expr, 'jax')

    m0 = jax.numpy.array([[1, 2, 3], [3, 2, 5], [5, 6, 7]])
    assert jax.numpy.linalg.matrix_rank(m0) == 3

    x0 = jax.numpy.array([3, 4, 5])

    assert jax.numpy.allclose(f_matsolve(m0, x0), f(m0, x0))

