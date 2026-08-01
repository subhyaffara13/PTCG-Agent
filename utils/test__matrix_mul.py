
def test_Matrix_mul():
    M = Matrix([[1, 2, 3], [x, y, x]])
    with ignore_warnings(PendingDeprecationWarning):
        m = matrix([[2, 4], [x, 6], [x, z**2]])
    assert M*m == Matrix([
        [         2 + 5*x,        16 + 3*z**2],
        [2*x + x*y + x**2, 4*x + 6*y + x*z**2],
    ])

    assert m*M == Matrix([
        [   2 + 4*x,      4 + 4*y,      6 + 4*x],
        [       7*x,    2*x + 6*y,          9*x],
        [x + x*z**2, 2*x + y*z**2, 3*x + x*z**2],
    ])
    a = array([2])
    assert a[0] * M == 2 * M
    assert M * a[0] == 2 * M

