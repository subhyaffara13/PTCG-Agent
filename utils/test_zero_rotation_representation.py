
def test_zero_rotation_representation(xp):
    r = Rotation.from_quat(xp.zeros((0, 4)))
    assert r.as_quat().shape == (0, 4)
    assert r.as_matrix().shape == (0, 3, 3)
    assert r.as_euler("xyz").shape == (0, 3)
    assert r.as_rotvec().shape == (0, 3)
    assert r.as_mrp().shape == (0, 3)
    assert r.as_davenport(xp.eye(3), "extrinsic").shape == (0, 3)

