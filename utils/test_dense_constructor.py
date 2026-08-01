
def test_dense_constructor():
    # 1d
    res1d = coo_array([1, 2, 3])
    assert res1d.shape == (3,)
    assert_equal(res1d.toarray(), np.array([1, 2, 3]))

    # 2d
    res2d = coo_array([[1, 2, 3], [4, 5, 6]])
    assert res2d.shape == (2, 3)
    assert_equal(res2d.toarray(), np.array([[1, 2, 3], [4, 5, 6]]))

    # 4d
    arr4d = np.array([[[[3, 7], [1, 0]], [[6, 5], [9, 2]]],
                      [[[4, 3], [2, 8]], [[7, 5], [1, 6]]],
                      [[[0, 9], [4, 3]], [[2, 1], [7, 8]]]])
    res4d = coo_array(arr4d)
    assert res4d.shape == (3, 2, 2, 2)
    assert_equal(res4d.toarray(), arr4d)

    # 9d
    np.random.seed(12)
    arr9d = np.random.randn(2,3,4,7,6,5,3,2,4)
    res9d = coo_array(arr9d)
    assert res9d.shape == (2,3,4,7,6,5,3,2,4)
    assert_equal(res9d.toarray(), arr9d)

    # storing nan as element of sparse array
    nan_3d = coo_array([[[1, np.nan]], [[3, 4]], [[5, 6]]])
    assert nan_3d.shape == (3, 1, 2)
    assert_equal(nan_3d.toarray(), np.array([[[1, np.nan]], [[3, 4]], [[5, 6]]]))

