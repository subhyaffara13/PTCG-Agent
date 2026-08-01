
def test_Matrix2():
    m = Matrix([[x, x**2], [5, 2/x]])
    with ignore_warnings(PendingDeprecationWarning):
        assert (matrix(m.subs(x, 2)) == matrix([[2, 4], [5, 1]])).all()
    m = Matrix([[sin(x), x**2], [5, 2/x]])
    with ignore_warnings(PendingDeprecationWarning):
        assert (matrix(m.subs(x, 2)) == matrix([[sin(2), 4], [5, 1]])).all()

