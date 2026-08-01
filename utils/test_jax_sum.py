
def test_jax_sum():
    if not jax:
        skip("JAX not installed")

    s = Sum(x ** i, (i, a, b))
    f = lambdify((a, b, x), s, 'jax')

    a_, b_ = 0, 10
    x_ = jax.numpy.linspace(-1, +1, 10)
    assert jax.numpy.allclose(f(a_, b_, x_), sum(x_ ** i_ for i_ in range(a_, b_ + 1)))

    s = Sum(i * x, (i, a, b))
    f = lambdify((a, b, x), s, 'jax')

    a_, b_ = 0, 10
    x_ = jax.numpy.linspace(-1, +1, 10)
    assert jax.numpy.allclose(f(a_, b_, x_), sum(i_ * x_ for i_ in range(a_, b_ + 1)))

