
def test_jax_hypot():
    if not jax:
        skip("JAX not installed")
    assert abs(lambdify((a, b), hypot(a, b), 'jax')(3, 4) - 5) <= JAX_DEFAULT_EPSILON

