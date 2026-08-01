
def test_jax_mod():
    if not jax:
        skip("JAX not installed")

    e = Mod(a, b)
    f = lambdify((a, b), e, 'jax')

    a_ = jax.numpy.array([0, 1, 2, 3])
    b_ = 2
    assert jax.numpy.array_equal(f(a_, b_), [0, 1, 0, 1])

    a_ = jax.numpy.array([0, 1, 2, 3])
    b_ = jax.numpy.array([2, 2, 2, 2])
    assert jax.numpy.array_equal(f(a_, b_), [0, 1, 0, 1])

    a_ = jax.numpy.array([2, 3, 4, 5])
    b_ = jax.numpy.array([2, 3, 4, 5])
    assert jax.numpy.array_equal(f(a_, b_), [0, 0, 0, 0])

