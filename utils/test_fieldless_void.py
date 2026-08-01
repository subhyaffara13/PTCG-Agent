
def test_fieldless_void():
    dt = np.dtype([])  # a void dtype with no fields
    x = np.empty(4, dt)

    # these arrays contain no values, so there's little to test - but this
    # shouldn't crash
    mx = np.ma.array(x)
    assert_equal(mx.dtype, x.dtype)
    assert_equal(mx.shape, x.shape)

    mx = np.ma.array(x, mask=x)
    assert_equal(mx.dtype, x.dtype)
    assert_equal(mx.shape, x.shape)

