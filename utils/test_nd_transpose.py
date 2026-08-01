
def test_nd_transpose(shape):
    rng = np.random.default_rng(23409823)

    arr = random_array(shape, density=0.6, rng=rng, dtype=int)
    exp_arr = arr.toarray().T
    trans_arr = arr.transpose()
    assert trans_arr.shape == shape[::-1]
    assert_equal(trans_arr.toarray(), exp_arr)

    if len(shape) >= 2:
        exp_arr = arr.toarray().mT
        trans_arr = arr.mT
        assert trans_arr.shape == exp_arr.shape
        assert_equal(trans_arr.toarray(), exp_arr)
    
        trans_arr = matrix_transpose(arr)
        assert trans_arr.shape == exp_arr.shape
        assert_equal(trans_arr.toarray(), exp_arr)
    else:
        with pytest.raises(ValueError, match="2-dimensional"):
            arr.mT
        with pytest.raises(ValueError, match="2-dimensional"):
            matrix_transpose(arr)

