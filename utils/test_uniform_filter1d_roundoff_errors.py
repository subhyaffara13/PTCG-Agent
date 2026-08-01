
def test_uniform_filter1d_roundoff_errors(xp):
    # gh-6930
    in_ = np.repeat([0, 1, 0], [9, 9, 9])
    in_ = xp.asarray(in_)

    for filter_size in range(3, 10):
        out = ndimage.uniform_filter1d(in_, filter_size)
        xp_assert_equal(xp.sum(out), xp.asarray(10 - filter_size), check_0d=False)

