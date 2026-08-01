
def test_num_jac():
    def fun(t, y):
        return np.vstack([
            -0.04 * y[0] + 1e4 * y[1] * y[2],
            0.04 * y[0] - 1e4 * y[1] * y[2] - 3e7 * y[1] ** 2,
            3e7 * y[1] ** 2
        ])

    def jac(t, y):
        return np.array([
            [-0.04, 1e4 * y[2], 1e4 * y[1]],
            [0.04, -1e4 * y[2] - 6e7 * y[1], -1e4 * y[1]],
            [0, 6e7 * y[1], 0]
        ])

    t = 1
    y = np.array([1, 0, 0])
    J_true = jac(t, y)
    threshold = 1e-5
    f = fun(t, y).ravel()

    J_num, factor = num_jac(fun, t, y, f, threshold, None)
    assert_allclose(J_num, J_true, rtol=1e-5, atol=1e-5)

    J_num, factor = num_jac(fun, t, y, f, threshold, factor)
    assert_allclose(J_num, J_true, rtol=1e-5, atol=1e-5)

