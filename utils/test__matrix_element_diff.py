
def test_MatrixElement_diff():
    assert (A[3, 0]*A[0, 0]).diff(A[0, 0]) == A[3, 0]

