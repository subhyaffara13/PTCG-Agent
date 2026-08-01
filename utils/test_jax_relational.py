
def test_jax_relational():
    if not jax:
        skip("JAX not installed")

    e = Equality(x, 1)

    f = lambdify((x,), e, 'jax')
    x_ = jax.numpy.array([0, 1, 2])
    assert jax.numpy.array_equal(f(x_), [False, True, False])

    e = Unequality(x, 1)

    f = lambdify((x,), e, 'jax')
    x_ = jax.numpy.array([0, 1, 2])
    assert jax.numpy.array_equal(f(x_), [True, False, True])

    e = (x < 1)

    f = lambdify((x,), e, 'jax')
    x_ = jax.numpy.array([0, 1, 2])
    assert jax.numpy.array_equal(f(x_), [True, False, False])

    e = (x <= 1)

    f = lambdify((x,), e, 'jax')
    x_ = jax.numpy.array([0, 1, 2])
    assert jax.numpy.array_equal(f(x_), [True, True, False])

    e = (x > 1)

    f = lambdify((x,), e, 'jax')
    x_ = jax.numpy.array([0, 1, 2])
    assert jax.numpy.array_equal(f(x_), [False, False, True])

    e = (x >= 1)

    f = lambdify((x,), e, 'jax')
    x_ = jax.numpy.array([0, 1, 2])
    assert jax.numpy.array_equal(f(x_), [False, True, True])

    # Multi-condition expressions
    e = (x >= 1) & (x < 2)
    f = lambdify((x,), e, 'jax')
    x_ = jax.numpy.array([0, 1, 2])
    assert jax.numpy.array_equal(f(x_), [False, True, False])

    e = (x >= 1) | (x < 2)
    f = lambdify((x,), e, 'jax')
    x_ = jax.numpy.array([0, 1, 2])
    assert jax.numpy.array_equal(f(x_), [True, True, True])

