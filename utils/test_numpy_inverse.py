
def test_numpy_inverse():
    if not numpy:
        skip("numpy not installed.")
    A = Matrix([[1, x], [0, 1]])
    f = lambdify((x), A**-1, modules="numpy")
    numpy.testing.assert_array_equal(f(2), numpy.array([[1, -2], [0,  1]]))

