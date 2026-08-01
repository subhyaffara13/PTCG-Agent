
def test_tril_indices():
    # indices without and with offset
    il1 = tril_indices(4)
    il2 = tril_indices(4, k=2)
    il3 = tril_indices(4, m=5)
    il4 = tril_indices(4, k=2, m=5)

    a = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12],
                  [13, 14, 15, 16]])
    b = np.arange(1, 21).reshape(4, 5)

    # indexing:
    assert_array_equal(a[il1],
                       array([1, 5, 6, 9, 10, 11, 13, 14, 15, 16]))
    assert_array_equal(b[il3],
                       array([1, 6, 7, 11, 12, 13, 16, 17, 18, 19]))

    # And for assigning values:
    a[il1] = -1
    assert_array_equal(a,
                       array([[-1, 2, 3, 4],
                              [-1, -1, 7, 8],
                              [-1, -1, -1, 12],
                              [-1, -1, -1, -1]]))
    b[il3] = -1
    assert_array_equal(b,
                       array([[-1, 2, 3, 4, 5],
                              [-1, -1, 8, 9, 10],
                              [-1, -1, -1, 14, 15],
                              [-1, -1, -1, -1, 20]]))
    # These cover almost the whole array (two diagonals right of the main one):
    a[il2] = -10
    assert_array_equal(a,
                       array([[-10, -10, -10, 4],
                              [-10, -10, -10, -10],
                              [-10, -10, -10, -10],
                              [-10, -10, -10, -10]]))
    b[il4] = -10
    assert_array_equal(b,
                       array([[-10, -10, -10, 4, 5],
                              [-10, -10, -10, -10, 10],
                              [-10, -10, -10, -10, -10],
                              [-10, -10, -10, -10, -10]]))

