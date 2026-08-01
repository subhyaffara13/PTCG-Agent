
def test_median_no_int_overflow(xp):
    # test integer overflow fix on example from gh-12836
    a = xp.asarray([65, 70], dtype=xp.int8)
    output = ndimage.median(a, labels=xp.ones((2,)), index=xp.asarray([1]))
    assert_array_almost_equal(output, xp.asarray([67.5]))

