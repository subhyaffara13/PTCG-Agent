
def test_from_davenport_broadcast(xp):
    rng = np.random.default_rng(0)
    # Create random, orthogonal axes
    r = Rotation.from_quat(xp.asarray(rng.normal(size=(4, 9, 1, 4))))
    axes = r.as_matrix()
    angles = xp.asarray(rng.normal(size=(1, 4, 3)))
    rot = Rotation.from_davenport(axes, 'e', angles)
    # (4, 9, 1, 3) + (3,) axes, (1, 4, 3) angles -> (4, 9, 4) + (4,) for quaternion
    assert rot.as_quat().shape == (4, 9, 4, 4)

