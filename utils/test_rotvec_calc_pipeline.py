
def test_rotvec_calc_pipeline(xp):
    # Include small angles
    rotvec = xp.asarray([
        [0, 0, 0],
        [1, -1, 2],
        [-3e-4, 3.5e-4, 7.5e-5]
        ])
    xp_assert_close(Rotation.from_rotvec(rotvec).as_rotvec(), rotvec)
    xp_assert_close(Rotation.from_rotvec(rotvec, degrees=True).as_rotvec(degrees=True),
                    rotvec)

