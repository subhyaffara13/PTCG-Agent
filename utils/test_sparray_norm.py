
def test_sparray_norm():
    row = np.array([0, 0, 1, 1])
    col = np.array([0, 1, 2, 3])
    data = np.array([4, 5, 7, 9])
    test_arr = scipy.sparse.coo_array((data, (row, col)), shape=(2, 4))
    test_mat = scipy.sparse.coo_matrix((data, (row, col)), shape=(2, 4))
    for ord in (1, np.inf, None):
        for ax in [0, 1, None, (0, 1), (1, 0)]:
            for A in (test_arr, test_mat):
                expected = npnorm(A.toarray(), ord=ord, axis=ax)
                actual = spnorm(A, ord=ord, axis=ax)
                assert hasattr(actual, "dtype")
                assert_equal(actual, expected)
    # test 1d array and 1d-like (column) matrix
    test_arr_1d = scipy.sparse.coo_array((data, (col,)), shape=(4,))
    test_mat_col = scipy.sparse.coo_matrix((data, (col, [0, 0, 0, 0])), shape=(4, 1))
    for ord in (1, np.inf, None):
        for ax in [0, None]:
            for A in (test_arr_1d, test_mat_col):
                expected = npnorm(A.toarray(), ord=ord, axis=ax)
                assert_equal(spnorm(A, ord=ord, axis=ax), expected)

