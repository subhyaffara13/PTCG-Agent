
def test_jax_multiple_sums():
    if not jax:
        skip("JAX not installed")

    s = Sum((x + j) * i, (i, a, b), (j, c, d))
    f = lambdify((a, b, c, d, x), s, 'jax')

    a_, b_ = 0, 10
    c_, d_ = 11, 21
    x_ = jax.numpy.linspace(-1, +1, 10)
    assert jax.numpy.allclose(f(a_, b_, c_, d_, x_),
                       sum((x_ + j_) * i_ for i_ in range(a_, b_ + 1) for j_ in range(c_, d_ + 1)))

