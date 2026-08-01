
def test_nd_tuple_constructor(shape):
    np.random.seed(12)
    arr = np.random.randn(*shape)
    res = coo_array(arr)
    assert res.shape == shape
    assert_equal(res.toarray(), arr)

