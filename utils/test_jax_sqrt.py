
def test_jax_sqrt():
    if not jax:
        skip("JAX not installed")
    assert abs(lambdify((a,), sqrt(a), 'jax')(4) - 2) <= JAX_DEFAULT_EPSILON

