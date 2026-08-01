
def test_as_rotvec_degrees(xp):
    # x->y, y->z, z->x
    mat = xp.asarray([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    rot = Rotation.from_matrix(mat)
    rotvec = rot.as_rotvec(degrees=True)
    angle = xp_vector_norm(rotvec, axis=-1)
    xp_assert_close(angle, xp.asarray(120.0)[()])
    xp_assert_close(rotvec[0], rotvec[1])
    xp_assert_close(rotvec[1], rotvec[2])

