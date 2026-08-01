
def test_as_generic_rotvec(xp):
    dtype = xpx.default_dtype(xp)
    atol = 1e-15 if dtype == xp.float64 else 1e-7
    quat = xp.asarray([
            [1, 2, -1, 0.5],
            [1, -1, 1, 0.0003],
            [0, 0, 0, 1]
            ])
    quat /= xp_vector_norm(quat, axis=-1, keepdims=True)

    rotvec = Rotation.from_quat(quat).as_rotvec()
    angle = xp_vector_norm(rotvec, axis=-1)

    xp_assert_close(quat[:, 3], xp.cos(angle / 2))
    xp_assert_close(xp.linalg.cross(rotvec, quat[:, :3]), xp.zeros((3, 3)), atol=atol)

