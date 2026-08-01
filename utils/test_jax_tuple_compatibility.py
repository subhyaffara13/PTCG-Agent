
def test_jax_tuple_compatibility():
    if not jax:
        skip("Jax not installed")

    x, y, z = symbols('x y z')
    expr = Max(x, y, z) + Min(x, y, z)
    func = lambdify((x, y, z), expr, 'jax')
    input_tuple1, input_tuple2 = (1, 2, 3), (4, 5, 6)
    input_array1, input_array2 = jax.numpy.asarray(input_tuple1), jax.numpy.asarray(input_tuple2)
    assert np.allclose(func(*input_tuple1), func(*input_array1))
    assert np.allclose(func(*input_tuple2), func(*input_array2))

