
def test_jax_log2():
    if not jax:
        skip("JAX not installed")
    assert abs(lambdify((a,), log2(a), 'jax')(256) - 8) <= JAX_DEFAULT_EPSILON

