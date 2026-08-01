
def test_sparse_addition(A):
    assert isinstance((A + A), scipy.sparse.sparray), "Expected array, got matrix"

