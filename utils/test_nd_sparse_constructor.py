
def test_nd_sparse_constructor(shape):
    empty_arr = coo_array(shape)
    res = coo_array(empty_arr)
    assert res.shape == (shape)
    assert_equal(res.toarray(), np.zeros(shape))

