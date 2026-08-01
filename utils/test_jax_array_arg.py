
def test_jax_array_arg():
    if not jax:
        skip("JAX not installed")

    f = lambdify([[x, y]], x*x + y, 'jax')
    result = f(jax.numpy.array([2.0, 1.0]))
    assert result == 5
    assert "jax" in str(type(result))

