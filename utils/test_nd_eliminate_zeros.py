
def test_nd_eliminate_zeros():
    # for 3d sparse arrays
    arr3d = coo_array(([1, 0, 0, 4], ([0, 1, 1, 2], [0, 1, 0, 1], [1, 1, 2, 0])))
    assert arr3d.nnz == 4
    assert arr3d.count_nonzero() == 2
    assert_equal(arr3d.toarray(), np.array([[[0, 1, 0], [0, 0, 0]],
                                    [[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [4, 0, 0]]]))
    arr3d.eliminate_zeros()
    assert arr3d.nnz == 2
    assert arr3d.count_nonzero() == 2
    assert_equal(arr3d.toarray(), np.array([[[0, 1, 0], [0, 0, 0]],
                                    [[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [4, 0, 0]]]))

    # for a 5d sparse array when all elements of data array are 0
    coords = ([0, 1, 1, 2], [0, 1, 0, 1], [1, 1, 2, 0], [0, 0, 2, 3], [1, 0, 0, 2])
    arr5d = coo_array(([0, 0, 0, 0], coords))
    assert arr5d.nnz == 4
    assert arr5d.count_nonzero() == 0
    arr5d.eliminate_zeros()
    assert arr5d.nnz == 0
    assert arr5d.count_nonzero() == 0
    assert_equal(arr5d.col, np.array([]))
    assert_equal(arr5d.row, np.array([]))
    assert_equal(arr5d.coords, ([], [], [], [], []))

