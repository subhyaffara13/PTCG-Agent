
def test_as_davenport(xp):
    dtype = xpx.default_dtype(xp)
    rnd = np.random.RandomState(0)
    n = 100
    angles = np.empty((n, 3))
    angles[:, 0] = rnd.uniform(low=-np.pi, high=np.pi, size=(n,))
    angles_middle = rnd.uniform(low=0, high=np.pi, size=(n,))
    angles[:, 2] = rnd.uniform(low=-np.pi, high=np.pi, size=(n,))
    lambdas = rnd.uniform(low=0, high=np.pi, size=(20,))

    e1 = xp.asarray([1.0, 0, 0])
    e2 = xp.asarray([0.0, 1, 0])

    for lamb in lambdas:
        e3 = xp.asarray(Rotation.from_rotvec(lamb*e2).apply(e1))
        ax_lamb = xp.stack([e1, e2, e3], axis=0)
        angles[:, 1] = angles_middle - lamb
        for order in ['extrinsic', 'intrinsic']:
            ax = ax_lamb if order == "intrinsic" else xp.flip(ax_lamb, axis=0)
            rot = Rotation.from_davenport(ax, order, xp.asarray(angles, dtype=dtype))
            angles_dav = rot.as_davenport(ax, order)
            xp_assert_close(angles_dav, xp.asarray(angles, dtype=dtype))

