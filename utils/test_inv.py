
def test_inv():
    B = MatrixSymbol('B', 3, 3)
    assert B.inv() == B**-1

    # https://github.com/sympy/sympy/issues/19162
    X = MatrixSymbol('X', 1, 1).as_explicit()
    assert X.inv() == Matrix([[1/X[0, 0]]])

    X = MatrixSymbol('X', 2, 2).as_explicit()
    detX = X[0, 0]*X[1, 1] - X[0, 1]*X[1, 0]
    invX = Matrix([[ X[1, 1], -X[0, 1]],
                   [-X[1, 0],  X[0, 0]]]) / detX
    assert X.inv() == invX


def test_inv(xp):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-7
    rnd = np.random.RandomState(0)
    n = 10
    # preserve use of old random_state during SPEC 7 transition
    p = Rotation.random(num=n, random_state=rnd)
    p = rotation_to_xp(p, xp)
    p_mat = p.as_matrix()
    q_mat = p.inv().as_matrix()

    result1 = p_mat @ q_mat
    result2 = q_mat @ p_mat

    eye3d = xp.empty((n, 3, 3))
    eye3d = xpx.at(eye3d)[..., :3, :3].set(xp.eye(3))

    xp_assert_close(result1, eye3d, atol=atol)
    xp_assert_close(result2, eye3d, atol=atol)

    # Batched version
    batch_shape = (10, 3, 7)
    atol = 1e-12 if dtype == xp.float64 else 1e-6
    quat = xp.asarray(rnd.normal(size=batch_shape + (4,)), dtype=dtype)
    r = Rotation.from_quat(quat)
    p_mat = r.as_matrix()
    q_mat = r.inv().as_matrix()
    result1 = p_mat @ q_mat
    result2 = q_mat @ p_mat
    eye_nd = xp.empty(batch_shape + (3, 3))
    eye_nd = xpx.at(eye_nd)[..., :3, :3].set(xp.eye(3))
    xp_assert_close(result1, eye_nd, atol=atol)
    xp_assert_close(result2, eye_nd, atol=atol)


def test_inv(B):
    if B.__class__.__name__[:3] != 'csc':
        return

    C = spla.inv(B)

    assert isinstance(C, scipy.sparse.sparray)
    npt.assert_allclose(C.todense(), np.linalg.inv(B.todense()))


def test_inv(matrices):
    A_dense, A_sparse, b = matrices
    x0 = splin.inv(sp.csc_array(A_dense))
    x = splin.inv(A_sparse)
    assert_allclose(x.todense(), x0.todense())

