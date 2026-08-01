
def test_nd_add_dense(shape):
    rng = np.random.default_rng(23409823)
    sp_x = random_array(shape, density=0.6, rng=rng, dtype=int)
    sp_y = random_array(shape, density=0.6, rng=rng, dtype=int)
    den_x, den_y = sp_x.toarray(), sp_y.toarray()
    exp = den_x + den_y
    res = sp_x + den_y
    assert type(res) is type(exp)
    assert_equal(res, exp)

