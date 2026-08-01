
def test_nd_matmul(mat_shape1, mat_shape2):
    rng = np.random.default_rng(23409823)

    sp_x = random_array(mat_shape1, density=0.6, random_state=rng, dtype=int)
    sp_y = random_array(mat_shape2, density=0.6, random_state=rng, dtype=int)
    den_x, den_y = sp_x.toarray(), sp_y.toarray()
    exp = den_x @ den_y
    # sparse-sparse
    res = sp_x @ sp_y
    assert_equal(res.toarray(), exp)
    # sparse-dense
    res = sp_x @ den_y
    assert_equal(res, exp)
    res = sp_x @ list(den_y)
    assert_equal(res, exp)

    # dense-sparse
    res = den_x @ sp_y
    assert_equal(res, exp)

