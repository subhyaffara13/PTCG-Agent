
def test_jax_codegen_extra():
    if not jax:
        skip("JAX not installed")

    M = MatrixSymbol("M", 2, 2)
    N = MatrixSymbol("N", 2, 2)
    P = MatrixSymbol("P", 2, 2)
    Q = MatrixSymbol("Q", 2, 2)
    ma = jax.numpy.array([[1, 2], [3, 4]])
    mb = jax.numpy.array([[1,-2], [-1, 3]])
    mc = jax.numpy.array([[2, 0], [1, 2]])
    md = jax.numpy.array([[1,-1], [4, 7]])

    cg = ArrayTensorProduct(M, N)
    f = lambdify((M, N), cg, 'jax')
    assert (f(ma, mb) == jax.numpy.einsum(ma, [0, 1], mb, [2, 3])).all()

    cg = ArrayAdd(M, N)
    f = lambdify((M, N), cg, 'jax')
    assert (f(ma, mb) == ma+mb).all()

    cg = ArrayAdd(M, N, P)
    f = lambdify((M, N, P), cg, 'jax')
    assert (f(ma, mb, mc) == ma+mb+mc).all()

    cg = ArrayAdd(M, N, P, Q)
    f = lambdify((M, N, P, Q), cg, 'jax')
    assert (f(ma, mb, mc, md) == ma+mb+mc+md).all()

    cg = PermuteDims(M, [1, 0])
    f = lambdify((M,), cg, 'jax')
    assert (f(ma) == ma.T).all()

    cg = PermuteDims(ArrayTensorProduct(M, N), [1, 2, 3, 0])
    f = lambdify((M, N), cg, 'jax')
    assert (f(ma, mb) == jax.numpy.transpose(jax.numpy.einsum(ma, [0, 1], mb, [2, 3]), (1, 2, 3, 0))).all()

    cg = ArrayDiagonal(ArrayTensorProduct(M, N), (1, 2))
    f = lambdify((M, N), cg, 'jax')
    assert (f(ma, mb) == jax.numpy.diagonal(jax.numpy.einsum(ma, [0, 1], mb, [2, 3]), axis1=1, axis2=2)).all()

