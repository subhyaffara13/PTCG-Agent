
def test_adjoint_trnaspose_conjugate():
    A = MatrixSymbol('A', n, n)
    assert A.transpose().inverse() == A.inverse().transpose()
    assert A.conjugate().inverse() == A.inverse().conjugate()
    assert A.adjoint().inverse() == A.inverse().adjoint()

