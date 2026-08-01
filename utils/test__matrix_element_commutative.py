
def test_MatrixElement_commutative():
    assert A[0, 1]*A[1, 0] == A[1, 0]*A[0, 1]

