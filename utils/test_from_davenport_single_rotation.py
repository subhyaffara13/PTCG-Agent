
def test_from_davenport_single_rotation(xp):
    axis = xp.asarray([0, 0, 1])
    quat = Rotation.from_davenport(axis, 'extrinsic', 90,
                                   degrees=True).as_quat()
    expected_quat = xp.asarray([0.0, 0, 1, 1]) / math.sqrt(2)
    xp_assert_close(quat, expected_quat)

