
def test_binary_dilation_noninteger_iterations(xp):
    # regression test for gh-9905, gh-9909: ValueError for
    # non integer iterations
    data = xp.ones([1])
    assert_raises(TypeError, ndimage.binary_dilation, data, iterations=0.5)
    assert_raises(TypeError, ndimage.binary_dilation, data, iterations=1.5)

