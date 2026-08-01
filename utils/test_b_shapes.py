
def test_b_shapes():
    # Test b being a scalar.
    A = np.array([[1.0, 2.0]])
    b = 3.0
    x = lsqr(A, b)[0]
    assert norm(A.dot(x) - b) == pytest.approx(0)

    # Test b being a column vector.
    A = np.eye(10)
    b = np.ones((10, 1))
    x = lsqr(A, b)[0]
    assert norm(A.dot(x) - b.ravel()) == pytest.approx(0)

