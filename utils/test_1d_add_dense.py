
def test_1d_add_dense():
    den_a = np.array([0, -2, -3, 0])
    den_b = np.array([0, 1, 2, 3])
    exp = den_a + den_b
    res = coo_array(den_a) + den_b
    assert type(res) is type(exp)
    assert_equal(res, exp)

