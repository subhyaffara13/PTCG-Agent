
def test_jax_dotproduct():
    if not jax:
        skip("JAX not installed")

    A = Matrix([x, y, z])
    f1 = lambdify([x, y, z], DotProduct(A, A), modules='jax')
    f2 = lambdify([x, y, z], DotProduct(A, A.T), modules='jax')
    f3 = lambdify([x, y, z], DotProduct(A.T, A), modules='jax')
    f4 = lambdify([x, y, z], DotProduct(A, A.T), modules='jax')

    assert f1(1, 2, 3) == \
        f2(1, 2, 3) == \
        f3(1, 2, 3) == \
        f4(1, 2, 3) == \
        jax.numpy.array([14])

