
def test_1d_tuple_constructor():
    res = coo_array(([9,8], ([1,2],)))
    assert res.shape == (3,)
    assert_equal(res.toarray(), np.array([0, 9, 8]))

