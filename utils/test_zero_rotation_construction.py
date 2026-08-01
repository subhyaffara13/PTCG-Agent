
def test_zero_rotation_construction(xp):
    r = Rotation.random(num=0)
    assert len(r) == 0

    r_ide = Rotation.identity(num=0)
    assert len(r_ide) == 0

    r_get = Rotation.random(num=3)[[]]
    assert len(r_get) == 0

    r_quat = Rotation.from_quat(xp.zeros((0, 4)))
    assert len(r_quat) == 0

    r_matrix = Rotation.from_matrix(xp.zeros((0, 3, 3)))
    assert len(r_matrix) == 0

    r_euler = Rotation.from_euler("xyz", xp.zeros((0, 3)))
    assert len(r_euler) == 0

    r_vec = Rotation.from_rotvec(xp.zeros((0, 3)))
    assert len(r_vec) == 0

    r_dav = Rotation.from_davenport(xp.eye(3), "extrinsic", xp.zeros((0, 3)))
    assert len(r_dav) == 0

    r_mrp = Rotation.from_mrp(xp.zeros((0, 3)))
    assert len(r_mrp) == 0

