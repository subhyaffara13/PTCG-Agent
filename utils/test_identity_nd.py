
def test_identity_nd(forward, backward, type, shape, axes, norm,
                     orthogonalize, xp):
    # Test the identity f^-1(f(x)) == x

    x = xp.asarray(np.random.random(shape))

    if axes is not None:
        shape = np.take(shape, axes)

    y = forward(x, type, axes=axes, norm=norm, orthogonalize=orthogonalize)
    z = backward(y, type, axes=axes, norm=norm, orthogonalize=orthogonalize)
    xp_assert_close(z, x)

    if axes is None:
        pad = [(0, 4)] * x.ndim
    elif isinstance(axes, int):
        pad = [(0, 0)] * x.ndim
        pad[axes] = (0, 4)
    else:
        pad = [(0, 0)] * x.ndim

        for a in axes:
            pad[a] = (0, 4)

    # TODO write an array-agnostic pad
    y2 = xp.asarray(np.pad(np.asarray(y), pad, mode='edge'))
    z2 = backward(y2, type, shape, axes, norm, orthogonalize=orthogonalize)
    xp_assert_close(z2, x)

