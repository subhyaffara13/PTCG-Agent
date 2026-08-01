
def test_sum_duplicates():
    # 1d case
    arr1d = coo_array(([2, 2, 2], ([1, 0, 1],)))
    assert arr1d.nnz == 3
    assert_equal(arr1d.toarray(), np.array([2, 4]))
    arr1d.sum_duplicates()
    assert arr1d.nnz == 2
    assert_equal(arr1d.toarray(), np.array([2, 4]))

    # 4d case
    arr4d = coo_array(([2, 3, 7], ([1, 0, 1], [0, 2, 0], [1, 2, 1], [1, 0, 1])))
    assert arr4d.nnz == 3
    expected = np.array(  # noqa: E501
        [[[[0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [3, 0]]],
         [[[0, 0], [0, 9], [0, 0]], [[0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0]]]]
    )
    assert_equal(arr4d.toarray(), expected)
    arr4d.sum_duplicates()
    assert arr4d.nnz == 2
    assert_equal(arr4d.toarray(), expected)

    # when there are no duplicates
    arr_nodups = coo_array(([1, 2, 3, 4], ([0, 1, 2, 3],)))
    assert arr_nodups.nnz == 4
    arr_nodups.sum_duplicates()
    assert arr_nodups.nnz == 4

