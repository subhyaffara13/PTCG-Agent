
def test_rank_regression_from_so():
    # see:
    # https://stackoverflow.com/questions/19072700/why-does-sympy-give-me-the-wrong-answer-when-i-row-reduce-a-symbolic-matrix

    nu, lamb = symbols('nu, lambda')
    A = Matrix([[-3*nu,         1,                  0,  0],
                [ 3*nu, -2*nu - 1,                  2,  0],
                [    0,      2*nu, (-1*nu) - lamb - 2,  3],
                [    0,         0,          nu + lamb, -3]])
    expected_reduced = Matrix([[1, 0, 0, 1/(nu**2*(-lamb - nu))],
                               [0, 1, 0,    3/(nu*(-lamb - nu))],
                               [0, 0, 1,         3/(-lamb - nu)],
                               [0, 0, 0,                      0]])
    expected_pivots = (0, 1, 2)

    reduced, pivots = A.rref()

    assert simplify(expected_reduced - reduced) == zeros(*A.shape)
    assert pivots == expected_pivots


def test_rank_regression_from_so():
    # see:
    # https://stackoverflow.com/questions/19072700/why-does-sympy-give-me-the-wrong-answer-when-i-row-reduce-a-symbolic-matrix

    nu, lamb = symbols('nu, lambda')
    A = Matrix([[-3*nu,         1,                  0,  0],
                [ 3*nu, -2*nu - 1,                  2,  0],
                [    0,      2*nu, (-1*nu) - lamb - 2,  3],
                [    0,         0,          nu + lamb, -3]])
    expected_reduced = Matrix([[1, 0, 0, 1/(nu**2*(-lamb - nu))],
                               [0, 1, 0,    3/(nu*(-lamb - nu))],
                               [0, 0, 1,         3/(-lamb - nu)],
                               [0, 0, 0,                      0]])
    expected_pivots = (0, 1, 2)

    reduced, pivots = A.rref()

    assert simplify(expected_reduced - reduced) == zeros(*A.shape)
    assert pivots == expected_pivots

