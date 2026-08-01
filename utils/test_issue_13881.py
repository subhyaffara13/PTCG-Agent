
def test_issue_13881():
    if not numpy:
        skip("numpy not installed.")

    X = MatrixSymbol('X', 3, 1)

    f = lambdify(X, X.T*X, 'numpy')
    assert f(numpy.array([1, 2, 3])) == 14
    assert f(numpy.array([3, 2, 1])) == 14

    f = lambdify(X, X*X.T, 'numpy')
    assert f(numpy.array([1, 2, 3])) == 14
    assert f(numpy.array([3, 2, 1])) == 14

    f = lambdify(X, (X*X.T)*X, 'numpy')
    arr1 = numpy.array([[1], [2], [3]])
    arr2 = numpy.array([[14],[28],[42]])

    assert numpy.array_equal(f(arr1), arr2)

