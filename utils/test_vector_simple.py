
def test_vector_simple():
    f = lambdify((x, y, z), (z, y, x))
    assert f(3, 2, 1) == (1, 2, 3)
    assert f(1.0, 2.0, 3.0) == (3.0, 2.0, 1.0)
    # make sure correct number of args required
    raises(TypeError, lambda: f(0))

