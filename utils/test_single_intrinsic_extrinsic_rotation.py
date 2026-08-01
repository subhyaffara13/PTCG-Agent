
def test_single_intrinsic_extrinsic_rotation(xp):
    extrinsic = Rotation.from_euler('z', xp.asarray(90), degrees=True).as_matrix()
    intrinsic = Rotation.from_euler('Z', xp.asarray(90), degrees=True).as_matrix()
    xp_assert_close(extrinsic, intrinsic)

