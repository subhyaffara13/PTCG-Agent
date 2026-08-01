
def test_Matrix_sum():
    M = Matrix([[1, 2, 3], [x, y, x], [2*y, -50, z*x]])
    with ignore_warnings(PendingDeprecationWarning):
        m = matrix([[2, 3, 4], [x, 5, 6], [x, y, z**2]])
    assert M + m == Matrix([[3, 5, 7], [2*x, y + 5, x + 6], [2*y + x, y - 50, z*x + z**2]])
    assert m + M == Matrix([[3, 5, 7], [2*x, y + 5, x + 6], [2*y + x, y - 50, z*x + z**2]])
    assert M + m == M.add(m)

