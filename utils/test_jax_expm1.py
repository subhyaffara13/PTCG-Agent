
def test_jax_expm1():
    if not jax:
        skip("JAX not installed")

    f = lambdify((a,), expm1(a), 'jax')
    assert abs(f(1e-10) - 1e-10 - 5e-21) <= 1e-10 * JAX_DEFAULT_EPSILON

