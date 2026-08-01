
def test_syequb():
    desired_log2s = np.array([0, 0, 0, 0, 0, 0, -1, -1, -2, -3])

    for ind, dtype in enumerate(DTYPES):
        A = np.eye(10, dtype=dtype)
        alpha = dtype(1. if ind < 2 else 1.j)
        d = np.array([alpha * 2.**x for x in range(-5, 5)], dtype=dtype)
        A += np.rot90(np.diag(d))

        syequb = get_lapack_funcs('syequb', dtype=dtype)
        s, scond, amax, info = syequb(A)

        assert_equal(np.log2(s).astype(int), desired_log2s)

