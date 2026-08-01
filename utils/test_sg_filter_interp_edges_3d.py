
def test_sg_filter_interp_edges_3d(xp):
    # Test mode='interp' with a 3-D array.
    t = xp.linspace(-5, 5, 21)
    delta = t[1] - t[0]
    x1 = xp.stack([t, -t])
    x2 = xp.stack([t ** 2, 3 * t ** 2 + 5])
    x3 = xp.stack([t ** 3, 2 * t ** 3 + t ** 2 - 0.5 * t])
    dx1 = xp.stack([xp.ones_like(t), -xp.ones_like(t)])
    dx2 = xp.stack([2 * t, 6 * t])
    dx3 = xp.stack([3 * t ** 2, 6 * t ** 2 + 2 * t - 0.5])

    # z has shape (3, 2, 21)
    z = xp.stack([x1, x2, x3])
    dz = xp.stack([dx1, dx2, dx3])

    y = savgol_filter(z, 7, 3, axis=-1, mode='interp', delta=delta)
    xp_assert_close(y, z, atol=1e-10)

    dy = savgol_filter(z, 7, 3, axis=-1, mode='interp', deriv=1, delta=delta)
    xp_assert_close(dy, dz, atol=1e-10)

    # z has shape (3, 21, 2)
    z = xp.stack([x1.T, x2.T, x3.T])
    dz = xp.stack([dx1.T, dx2.T, dx3.T])

    y = savgol_filter(z, 7, 3, axis=1, mode='interp', delta=delta)
    xp_assert_close(y, z, atol=1e-10)

    dy = savgol_filter(z, 7, 3, axis=1, mode='interp', deriv=1, delta=delta)
    xp_assert_close(dy, dz, atol=1e-10)

    # z has shape (21, 3, 2)
    z = xp.asarray(xp_swapaxes(z, 0, 1, xp=xp), copy=True)
    dz = xp.asarray(xp_swapaxes(dz, 0, 1, xp=xp), copy=True)

    y = savgol_filter(z, 7, 3, axis=0, mode='interp', delta=delta)
    xp_assert_close(y, z, atol=1e-10)

    dy = savgol_filter(z, 7, 3, axis=0, mode='interp', deriv=1, delta=delta)
    xp_assert_close(dy, dz, atol=1e-10)

