
def test_jax_exp2():
    if not jax:
        skip("JAX not installed")
    assert abs(lambdify((a,), exp2(a), 'jax')(5) - 32) <= JAX_DEFAULT_EPSILON

