
def test_Matrix4():
    with ignore_warnings(PendingDeprecationWarning):
        a = matrix([[2, 4], [5, 1]])
    assert Matrix(a) == Matrix([[2, 4], [5, 1]])
    assert Matrix(a) != Matrix([[2, 4], [5, 2]])
    with ignore_warnings(PendingDeprecationWarning):
        a = matrix([[sin(2), 4], [5, 1]])
    assert Matrix(a) == Matrix([[sin(2), 4], [5, 1]])
    assert Matrix(a) != Matrix([[sin(0), 4], [5, 1]])

