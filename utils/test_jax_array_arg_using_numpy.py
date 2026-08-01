
def test_jax_array_arg_using_numpy():
    if not jax:
        skip("JAX not installed")

    f = lambdify([[x, y]], x*x + y, 'numpy')
    result = f(jax.numpy.array([2.0, 1.0]))
    assert result == 5
    assert "jax" in str(type(result))

