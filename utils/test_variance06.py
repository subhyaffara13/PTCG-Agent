
def test_variance06(xp):
    labels = xp.asarray([2, 2, 3, 3, 4])
    with np.errstate(all='ignore'):
        for type in types:
            dtype = getattr(xp, type)
            input = xp.asarray([1, 3, 8, 10, 8], dtype=dtype)
            output = ndimage.variance(input, labels, xp.asarray([2, 3, 4]))
            assert_array_almost_equal(output, xp.asarray([1.0, 1.0, 0.0]))

