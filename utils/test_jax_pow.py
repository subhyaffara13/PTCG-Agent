
def test_jax_pow():
    if not jax:
        skip('JAX not installed')

    expr = Pow(2, -1, evaluate=False)
    f = lambdify([], expr, 'jax')
    assert f() == 0.5

