
def test_identity_nd_overwrite(forward, backward, type, shape, axes, dtype,
                               norm, overwrite_x):
    # Test the identity f^-1(f(x)) == x

    x = np.random.random(shape).astype(dtype)
    x_orig = x.copy()

    if axes is not None:
        shape = np.take(shape, axes)

    y = forward(x, type, axes=axes, norm=norm)
    y_orig = y.copy()
    z = backward(y, type, axes=axes, norm=norm)
    if overwrite_x:
        assert_allclose(z, x_orig, rtol=1e-6, atol=1e-6)
    else:
        assert_allclose(z, x, rtol=1e-6, atol=1e-6)
        assert_array_equal(x, x_orig)
        assert_array_equal(y, y_orig)

