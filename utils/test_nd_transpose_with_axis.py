
def test_nd_transpose_with_axis(shape, axis_perm):
    rng = np.random.default_rng(23409823)

    arr = random_array(shape, density=0.6, rng=rng, dtype=int)
    trans_arr = arr.transpose(axes=axis_perm)
    assert_equal(trans_arr.toarray(), np.transpose(arr.toarray(), axes=axis_perm))

