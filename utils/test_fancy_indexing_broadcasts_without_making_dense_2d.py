
def test_fancy_indexing_broadcasts_without_making_dense_2d(cls):
    # Fixes Issue gh-24339
    J = np.arange(100_000)
    I = J.reshape((100_000, 1))
    S = cls((100_000, 100_000))
    # checking nnz, but really testing indexing.
    assert S[I, J].nnz == 0  # 1D row array for columns -> broadcasts to 2D
    assert S[I, J.reshape(1, -1)].nnz == 0  # 2D row array as index for columns

