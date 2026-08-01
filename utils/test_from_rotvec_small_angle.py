
def test_from_rotvec_small_angle(xp):
    rotvec = xp.asarray([
        [5e-4 / math.sqrt(3), -5e-4 / math.sqrt(3), 5e-4 / math.sqrt(3)],
        [0.2, 0.3, 0.4],
        [0, 0, 0]
        ])

    quat = Rotation.from_rotvec(rotvec).as_quat()
    # cos(theta/2) ~~ 1 for small theta
    xp_assert_close(quat[0, 3], xp.asarray(1.0)[()])
    # sin(theta/2) / theta ~~ 0.5 for small theta
    xp_assert_close(quat[0, :3], rotvec[0, ...] * 0.5)

    xp_assert_close(quat[1, 3], xp.asarray(0.9639685)[()])
    xp_assert_close(quat[1, :3],
            xp.asarray([
                0.09879603932153465,
                0.14819405898230198,
                0.19759207864306931]))

    xp_assert_equal(quat[2, ...], xp.asarray([0.0, 0, 0, 1]))

