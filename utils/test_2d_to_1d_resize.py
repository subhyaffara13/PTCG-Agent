
def test_2d_to_1d_resize(arg: int):
    den = np.array([[1, 0, 3], [4, 0, 0]])
    res = coo_array(den)
    den.resize(arg, refcheck=False)
    res.resize(arg)
    assert res.shape == den.shape
    assert_equal(res.toarray(), den)

