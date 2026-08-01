
def test_from_davenport_one_or_two_axes(xp):
    ez = xp.asarray([0.0, 0, 1])
    ey = xp.asarray([0.0, 1, 0])

    # Single rotation, single axis, axes.shape == (3, )
    rot = Rotation.from_rotvec(ez * xp.pi/4)
    rot_dav = Rotation.from_davenport(ez, 'e', xp.pi/4)
    xp_assert_close(rot.as_quat(canonical=True), rot_dav.as_quat(canonical=True))

    # Single rotation, single axis, axes.shape == (1, 3), angles.shape == (1, )
    # -> Still single rotation
    axes = xp.reshape(ez, (1, 3))  # Torch can't create tensors from xp.asarray([ez])
    rot = Rotation.from_rotvec(ez * xp.pi/4)
    rot_dav = Rotation.from_davenport(axes, 'e', [xp.pi/4])
    xp_assert_close(rot.as_quat(canonical=True), rot_dav.as_quat(canonical=True))

    # Single rotation, two axes, axes.shape == (2, 3)
    axes = xp.stack([ez, ey], axis=0)
    rot = Rotation.from_rotvec(axes * xp.asarray([[xp.pi/4], [xp.pi/6]]))
    rot = rot[0] * rot[1]
    axes_dav = xp.stack([ey, ez], axis=0)
    rot_dav = Rotation.from_davenport(axes_dav, 'e', [xp.pi/6, xp.pi/4])
    xp_assert_close(rot.as_quat(canonical=True), rot_dav.as_quat(canonical=True))

    # Two rotations, single axis, axes.shape == (3, )
    axes = xp.stack([ez, ez], axis=0)
    rot = Rotation.from_rotvec(axes * xp.asarray([[xp.pi/6], [xp.pi/4]]))
    axes_dav = xp.reshape(ez, (1, 3))
    rot_dav = Rotation.from_davenport(axes_dav, 'e', [[xp.pi/6], [xp.pi/4]])
    xp_assert_close(rot.as_quat(canonical=True), rot_dav.as_quat(canonical=True))

