
def test_jax_log10():
    if not jax:
        skip("JAX not installed")

    assert abs(lambdify((a,), log10(a), 'jax')(100) - 2) <= JAX_DEFAULT_EPSILON

