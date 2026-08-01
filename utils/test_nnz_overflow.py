
def test_nnz_overflow():
    # Regression test for gh-7230 / gh-7871, checking that coo_toarray
    # with nnz > int32max doesn't overflow.
    nnz = np.iinfo(np.int32).max + 1
    # Ensure ~20 GB of RAM is free to run this test.
    check_free_memory((4 + 4 + 1) * nnz / 1e6 + 0.5)

    # Use nnz duplicate entries to keep the dense version small.
    row = np.zeros(nnz, dtype=np.int32)
    col = np.zeros(nnz, dtype=np.int32)
    data = np.zeros(nnz, dtype=np.int8)
    data[-1] = 4
    s = coo_matrix((data, (row, col)), shape=(1, 1), copy=False)
    # Sums nnz duplicates to produce a 1x1 array containing 4.
    d = s.toarray()

    assert_allclose(d, [[4]])

