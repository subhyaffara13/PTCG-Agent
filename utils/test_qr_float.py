
def test_QR_float():
    A = Matrix([[1, 1], [1, 1.01]])
    Q, R = A.QRdecomposition()
    assert allclose(Q * R, A)
    assert allclose(Q * Q.T, Matrix.eye(2))
    assert allclose(Q.T * Q, Matrix.eye(2))

    A = Matrix([[1, 1], [1, 1.001]])
    Q, R = A.QRdecomposition()
    assert allclose(Q * R, A)
    assert allclose(Q * Q.T, Matrix.eye(2))
    assert allclose(Q.T * Q, Matrix.eye(2))

