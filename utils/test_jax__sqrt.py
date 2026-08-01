
def test_jax_Sqrt():
    if not jax:
        skip("JAX not installed")
    assert abs(lambdify((a,), Sqrt(a), 'jax')(4) - 2) <= JAX_DEFAULT_EPSILON

