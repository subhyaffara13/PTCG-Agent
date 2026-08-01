
def test_dense_divide(A):
    assert isinstance((A / 2), scipy.sparse.sparray), "Expected array, got matrix"

