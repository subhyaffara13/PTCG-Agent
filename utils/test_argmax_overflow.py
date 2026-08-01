
def test_argmax_overflow(ax):
    # See gh-13646: Windows integer overflow for large sparse matrices.
    dim = (100000, 100000)
    A = lil_matrix(dim)
    A[-2, -2] = 42
    A[-3, -3] = 0.1234
    A = csc_matrix(A)
    idx = A.argmax(axis=ax)

    if ax is None:
        # idx is a single flattened index
        # that we need to convert to a 2d index pair;
        # can't do this with np.unravel_index because
        # the dimensions are too large
        ii = idx % dim[0]
        jj = idx // dim[0]
    else:
        # idx is an array of size of A.shape[ax];
        # check the max index to make sure no overflows
        # we encountered
        assert np.count_nonzero(idx) == A.nnz
        ii, jj = np.max(idx), np.argmax(idx)

    assert A[ii, jj] == A[-2, -2]

