
def test_inv_single_rotation(xp):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-7
    rng = np.random.default_rng(146972845698875399755764481408308808739)
    p = rotation_to_xp(Rotation.random(rng=rng), xp)
    q = p.inv()

    p_mat = p.as_matrix()
    q_mat = q.as_matrix()
    res1 = xp.matmul(p_mat, q_mat)
    res2 = xp.matmul(q_mat, p_mat)

    eye = xp.eye(3)

    xp_assert_close(res1, eye, atol=atol)
    xp_assert_close(res2, eye, atol=atol)

    x = rotation_to_xp(Rotation.random(num=1, rng=rng), xp)
    y = x.inv()

    x_matrix = x.as_matrix()
    y_matrix = y.as_matrix()
    result1 = xp.linalg.matmul(x_matrix, y_matrix)
    result2 = xp.linalg.matmul(y_matrix, x_matrix)

    eye3d = xp.empty((1, 3, 3))
    eye3d = xpx.at(eye3d)[..., :3, :3].set(xp.eye(3))

    xp_assert_close(result1, eye3d, atol=atol)
    xp_assert_close(result2, eye3d, atol=atol)

