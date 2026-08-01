
def test_as_davenport_degenerate(xp, suppress_warnings):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-6
    # Since we cannot check for angle equality, we check for rotation matrix
    # equality
    rnd = np.random.RandomState(0)
    n = 5
    angles = np.empty((n, 3))

    # symmetric sequences
    angles[:, 0] = rnd.uniform(low=-np.pi, high=np.pi, size=(n,))
    angles_middle = [rnd.choice([0, np.pi]) for i in range(n)]
    angles[:, 2] = rnd.uniform(low=-np.pi, high=np.pi, size=(n,))
    lambdas = rnd.uniform(low=0, high=np.pi, size=(5,))

    e1 = xp.asarray([1.0, 0, 0])
    e2 = xp.asarray([0.0, 1, 0])

    for lamb in lambdas:
        e3 = xp.asarray(Rotation.from_rotvec(lamb*e2).apply(e1))
        ax_lamb = xp.stack([e1, e2, e3], axis=0)
        angles[:, 1] = angles_middle - lamb
        for order in ['extrinsic', 'intrinsic']:
            ax = ax_lamb if order == 'intrinsic' else xp.flip(ax_lamb, axis=0)
            rot = Rotation.from_davenport(ax, order, xp.asarray(angles, dtype=dtype))
            with maybe_warn_gimbal_lock(not suppress_warnings, xp):
                angles_dav = rot.as_davenport(
                    ax,
                    order,
                    suppress_warnings=suppress_warnings
                )
            mat_expected = rot.as_matrix()
            rot_estimated = Rotation.from_davenport(ax, order, angles_dav)
            mat_estimated = rot_estimated.as_matrix()
            xp_assert_close(mat_expected, mat_estimated, atol=atol)

