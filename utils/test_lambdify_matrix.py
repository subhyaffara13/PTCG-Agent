
def test_lambdify_matrix():
    f = lambdify(x, Matrix([[x, 2*x], [1, 2]]), [{'ImmutableMatrix': numpy.array}, "numpy"])
    assert (f(1) == array([[1, 2], [1, 2]])).all()

