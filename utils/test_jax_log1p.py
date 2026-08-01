
def test_jax_log1p():
    if not jax:
        skip("JAX not installed")

    f = lambdify((a,), log1p(a), 'jax')
    assert abs(f(1e-99) - 1e-99) <= 1e-99 * JAX_DEFAULT_EPSILON

