
def test_identity_1d(forward, backward, type, n, axis, norm, orthogonalize, xp):
    # Test the identity f^-1(f(x)) == x
    x = xp.asarray(np.random.rand(n, n))

    y = forward(x, type, axis=axis, norm=norm, orthogonalize=orthogonalize)
    z = backward(y, type, axis=axis, norm=norm, orthogonalize=orthogonalize)
    xp_assert_close(z, x)

    pad = [(0, 0)] * 2
    pad[axis] = (0, 4)

    y2 = xp.asarray(np.pad(np.asarray(y), pad, mode='edge'))
    z2 = backward(y2, type, n, axis, norm, orthogonalize=orthogonalize)
    xp_assert_close(z2, x)

