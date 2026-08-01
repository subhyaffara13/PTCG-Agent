
def test_nd_matmul_vector(mat_shape, vec_shape):
    rng = np.random.default_rng(23409823)

    sp_x = random_array(mat_shape, density=0.6, rng=rng, dtype=int)
    sp_y = random_array(vec_shape, density=0.6, rng=rng, dtype=int)
    den_x, den_y = sp_x.toarray(), sp_y.toarray()
    exp = den_x @ den_y
    res = sp_x @ den_y
    assert_equal(res,exp)
    res = sp_x @ list(den_y)
    assert_equal(res,exp)

