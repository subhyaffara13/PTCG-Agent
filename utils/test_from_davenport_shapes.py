
def test_from_davenport_shapes(xp, ndim: int):
    # The shape rules for ND rotations are as follows:
    # axes.shape[-2] must be angles.shape[-1]
    # Resulting shape is np.broadcast_shapes(axes.shape[:-2], angles.shape[:-1]) + (4,)
    rng = np.random.default_rng(0)
    batch_shape = (ndim,) * (ndim - 1)
    # Create random, orthogonal axes
    r = Rotation.from_quat(xp.asarray(rng.normal(size=(4,))))
    axes = r.as_matrix()
    # axes = (3,)
    angles = xp.asarray(rng.normal(size=batch_shape + (1,)))
    rot = Rotation.from_davenport(axes[0, ...], 'e', angles)
    assert rot.as_quat().shape == batch_shape + (4,)
    # axes = (1, 3)
    angles = xp.asarray(rng.normal(size=batch_shape + (1,)))
    rot = Rotation.from_davenport(axes[0, None, ...], 'e', angles)
    assert rot.as_quat().shape == batch_shape + (4,)
    # axes = (2, 3)
    angles = xp.asarray(rng.normal(size=batch_shape + (2,)))
    rot = Rotation.from_davenport(axes[:2, ...], 'e', angles)
    assert rot.as_quat().shape == batch_shape + (4,)

    # axes = (...,3, 3)
    r = Rotation.from_quat(xp.asarray(rng.normal(size=batch_shape + (4,))))
    axes = r.as_matrix()
    angles = xp.asarray(rng.normal(size=batch_shape + (3,)))
    rot = Rotation.from_davenport(axes, 'e', angles)
    assert rot.as_quat().shape == batch_shape + (4,)

