
def test_binary_opening_noninteger_iterations(xp):
    # regression test for gh-9905, gh-9909: ValueError for
    # non integer iterations
    data = xp.ones([1])
    assert_raises(TypeError, ndimage.binary_opening, data, iterations=0.5)
    assert_raises(TypeError, ndimage.binary_opening, data, iterations=1.5)

