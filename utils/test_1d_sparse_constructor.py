
def test_1d_sparse_constructor():
    empty1d = coo_array((3,))
    res = coo_array(empty1d)
    assert res.shape == (3,)
    assert_equal(res.toarray(), np.zeros((3,)))

