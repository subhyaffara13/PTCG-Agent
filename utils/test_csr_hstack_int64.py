
def test_csr_hstack_int64():
    """
    Tests if hstack properly promotes to indices and indptr arrays to np.int64
    when using np.int32 during concatenation would result in either array
    overflowing.
    """
    max_int32 = np.iinfo(np.int32).max

    # First case: indices would overflow with int32
    data = [1.0]
    row = [0]

    max_indices_1 = max_int32 - 1
    max_indices_2 = 3

    # Individual indices arrays are representable with int32
    col_1 = [max_indices_1 - 1]
    col_2 = [max_indices_2 - 1]

    X_1 = csr_matrix((data, (row, col_1)))
    X_2 = csr_matrix((data, (row, col_2)))

    assert max(max_indices_1 - 1, max_indices_2 - 1) < max_int32
    assert X_1.indices.dtype == X_1.indptr.dtype == np.int32
    assert X_2.indices.dtype == X_2.indptr.dtype == np.int32

    # ... but when concatenating their CSR matrices, the resulting indices
    # array can't be represented with int32 and must be promoted to int64.
    X_hs = hstack([X_1, X_2], format="csr")

    assert X_hs.indices.max() == max_indices_1 + max_indices_2 - 1
    assert max_indices_1 + max_indices_2 - 1 > max_int32
    assert X_hs.indices.dtype == X_hs.indptr.dtype == np.int64

    # Even if the matrices are empty, we must account for their size
    # contribution so that we may safely set the final elements.
    X_1_empty = csr_matrix(X_1.shape)
    X_2_empty = csr_matrix(X_2.shape)
    X_hs_empty = hstack([X_1_empty, X_2_empty], format="csr")

    assert X_hs_empty.shape == X_hs.shape
    assert X_hs_empty.indices.dtype == np.int64

    # Should be just small enough to stay in int32 after stack. Note that
    # we theoretically could support indices.max() == max_int32, but due to an
    # edge-case in the underlying sparsetools code
    # (namely the `coo_tocsr` routine),
    # we require that max(X_hs_32.shape) < max_int32 as well.
    # Hence we can only support max_int32 - 1.
    col_3 = [max_int32 - max_indices_1 - 1]
    X_3 = csr_matrix((data, (row, col_3)))
    X_hs_32 = hstack([X_1, X_3], format="csr")
    assert X_hs_32.indices.dtype == np.int32
    assert X_hs_32.indices.max() == max_int32 - 1

