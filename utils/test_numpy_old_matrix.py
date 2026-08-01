
def test_numpy_old_matrix():
    if not numpy:
        skip("numpy not installed.")
    A = Matrix([[x, x*y], [sin(z) + 4, x**z]])
    sol_arr = numpy.array([[1, 2], [numpy.sin(3) + 4, 1]])
    f = lambdify((x, y, z), A, [{'ImmutableDenseMatrix': numpy.matrix}, 'numpy'])
    with ignore_warnings(PendingDeprecationWarning):
        numpy.testing.assert_allclose(f(1, 2, 3), sol_arr)
        assert isinstance(f(1, 2, 3), numpy.matrix)

