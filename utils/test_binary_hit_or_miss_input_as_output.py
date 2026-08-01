
def test_binary_hit_or_miss_input_as_output(xp):
    rstate = np.random.RandomState(123)
    data = rstate.randint(low=0, high=2, size=100).astype(bool)
    data = xp.asarray(data)

    # input data is not modified
    data_orig = data.copy()
    expected = ndimage.binary_hit_or_miss(data)
    xp_assert_equal(data, data_orig)

    # data should now contain the expected result
    ndimage.binary_hit_or_miss(data, output=data)
    xp_assert_equal(data, expected)

