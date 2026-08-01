
def test_from_matrix_ortho_output(xp):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-6
    rnd = np.random.RandomState(0)
    mat = xp.asarray(rnd.random_sample((100, 3, 3)), dtype=dtype)
    dets = xp.linalg.det(mat)
    for i in range(dets.shape[0]):
        # Make sure we have a right-handed rotation matrix
        if dets[i] < 0:
            mat = xpx.at(mat)[i, ...].set(-mat[i, ...])
    ortho_mat = Rotation.from_matrix(mat).as_matrix()

    mult_result = xp.matmul(ortho_mat, xp.matrix_transpose(ortho_mat))

    eye3d = xp.zeros((100, 3, 3)) + xp.eye(3)
    xp_assert_close(mult_result, eye3d, atol=atol)

