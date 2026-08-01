
def test_jax_codegen_einsum():
    if not jax:
        skip("JAX not installed")

    M = MatrixSymbol("M", 2, 2)
    N = MatrixSymbol("N", 2, 2)

    cg = convert_matrix_to_array(M * N)
    f = lambdify((M, N), cg, 'jax')

    ma = jax.numpy.array([[1, 2], [3, 4]])
    mb = jax.numpy.array([[1,-2], [-1, 3]])
    assert (f(ma, mb) == jax.numpy.matmul(ma, mb)).all()

