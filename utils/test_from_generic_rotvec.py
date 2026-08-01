
def test_from_generic_rotvec(xp):
    atol = 1e-7
    rotvec = xp.asarray([
            [1, 2, 2],
            [1, -1, 0.5],
            [0, 0, 0]])
    expected_quat = xp.asarray([
        [0.3324983, 0.6649967, 0.6649967, 0.0707372],
        [0.4544258, -0.4544258, 0.2272129, 0.7316889],
        [0, 0, 0, 1]
        ])
    xp_assert_close(Rotation.from_rotvec(rotvec).as_quat(), expected_quat, atol=atol)

