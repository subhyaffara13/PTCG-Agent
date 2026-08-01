
def test_nd_reshape(shape, new_shape):
    # reshaping a 4d sparse array
    rng = np.random.default_rng(23409823)

    arr4d = random_array(shape, density=0.6, rng=rng, dtype=int)
    assert arr4d.shape == shape
    den4d = arr4d.toarray()

    exp_arr = den4d.reshape(new_shape)
    res_arr = arr4d.reshape(new_shape)
    assert res_arr.shape == new_shape
    assert_equal(res_arr.toarray(), exp_arr)

