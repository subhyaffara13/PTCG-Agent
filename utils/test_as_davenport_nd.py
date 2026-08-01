
def test_as_davenport_nd(xp):
    rng = np.random.default_rng(0)
    r = Rotation.from_quat(xp.asarray(rng.normal(size=(4, 9, 1, 4))))
    axes = r.as_matrix()  # Get orthogonal axes
    angles = xp.asarray(rng.uniform(low=-np.pi, high=np.pi, size=(4, 9, 1, 3)))
    angles = xpx.at(angles)[..., 1].set(angles[..., 1] / 2)

    for order in ['extrinsic', 'intrinsic']:
        if order == "intrinsic":
            axes = xp.flip(axes, axis=-2)
        rot = Rotation.from_davenport(axes, order, angles)
        angles_dav = rot.as_davenport(axes, order)
        xp_assert_close(angles_dav, angles)

