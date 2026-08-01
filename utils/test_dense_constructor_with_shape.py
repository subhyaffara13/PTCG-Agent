
def test_dense_constructor_with_shape():
    res1d = coo_array([1, 2, 3], shape=(3,))
    assert res1d.shape == (3,)
    assert_equal(res1d.toarray(), np.array([1, 2, 3]))

    res2d = coo_array([[1, 2, 3], [4, 5, 6]], shape=(2, 3))
    assert res2d.shape == (2, 3)
    assert_equal(res2d.toarray(), np.array([[1, 2, 3], [4, 5, 6]]))

    res3d = coo_array([[[3]], [[4]]], shape=(2, 1, 1))
    assert res3d.shape == (2, 1, 1)
    assert_equal(res3d.toarray(), np.array([[[3]], [[4]]]))

    np.random.seed(12)
    arr7d = np.random.randn(2,4,1,6,5,3,2)
    res7d = coo_array((arr7d), shape=(2,4,1,6,5,3,2))
    assert res7d.shape == (2,4,1,6,5,3,2)
    assert_equal(res7d.toarray(), arr7d)

