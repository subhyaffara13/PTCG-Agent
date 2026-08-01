
def test_sparse_dense_divide(A):
    with pytest.warns(RuntimeWarning):
        assert isinstance((A / A.todense()), scipy.sparse.sparray)

