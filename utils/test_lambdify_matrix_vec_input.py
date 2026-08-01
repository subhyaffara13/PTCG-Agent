
def test_lambdify_matrix_vec_input():
    X = sympy.DeferredVector('X')
    M = Matrix([
        [X[0]**2, X[0]*X[1], X[0]*X[2]],
        [X[1]*X[0], X[1]**2, X[1]*X[2]],
        [X[2]*X[0], X[2]*X[1], X[2]**2]])
    f = lambdify(X, M, [{'ImmutableMatrix': numpy.array}, "numpy"])

    Xh = array([1.0, 2.0, 3.0])
    expected = array([[Xh[0]**2, Xh[0]*Xh[1], Xh[0]*Xh[2]],
                      [Xh[1]*Xh[0], Xh[1]**2, Xh[1]*Xh[2]],
                      [Xh[2]*Xh[0], Xh[2]*Xh[1], Xh[2]**2]])
    actual = f(Xh)
    assert numpy.allclose(actual, expected)

