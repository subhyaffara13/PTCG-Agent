
def test_matrix_transform():
    A = matrix([[1, 2], [3, 4], [5, 6]])
    assert A.T == A.transpose() == matrix([[1, 3, 5], [2, 4, 6]])
    swap_row(A, 1, 2)
    assert A == matrix([[1, 2], [5, 6], [3, 4]])
    l = [1, 2]
    swap_row(l, 0, 1)
    assert l == [2, 1]
    assert extend(eye(3), [1,2,3]) == matrix([[1,0,0,1],[0,1,0,2],[0,0,1,3]])

