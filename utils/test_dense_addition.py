
def test_dense_addition(A):
    X = np.random.random(A.shape)
    assert not isinstance(A + X, np.matrix), "Expected array, got matrix"

