
def test_identity_1d_overwrite(forward, backward, type, dtype, axis, norm,
                               overwrite_x):
    # Test the identity f^-1(f(x)) == x
    x = np.random.rand(7, 8).astype(dtype)
    x_orig = x.copy()

    y = forward(x, type, axis=axis, norm=norm, overwrite_x=overwrite_x)
    y_orig = y.copy()
    z = backward(y, type, axis=axis, norm=norm, overwrite_x=overwrite_x)
    if not overwrite_x:
        assert_allclose(z, x, rtol=1e-6, atol=1e-6)
        assert_array_equal(x, x_orig)
        assert_array_equal(y, y_orig)
    else:
        assert_allclose(z, x_orig, rtol=1e-6, atol=1e-6)

