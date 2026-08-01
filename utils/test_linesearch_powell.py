
def test_linesearch_powell():
    # helper function in optimize.py, not a public function.
    linesearch_powell = optimize._optimize._linesearch_powell
    # args are func, p, xi, fval, lower_bound=None, upper_bound=None, tol=1e-3
    # returns new_fval, p + direction, direction
    def func(x):
        return np.sum((x - np.array([-1.0, 2.0, 1.5, -0.4])) ** 2)
    p0 = np.array([0., 0, 0, 0])
    fval = func(p0)
    lower_bound = np.array([-np.inf] * 4)
    upper_bound = np.array([np.inf] * 4)

    all_tests = (
        (np.array([1., 0, 0, 0]), -1),
        (np.array([0., 1, 0, 0]), 2),
        (np.array([0., 0, 1, 0]), 1.5),
        (np.array([0., 0, 0, 1]), -.4),
        (np.array([-1., 0, 1, 0]), 1.25),
        (np.array([0., 0, 1, 1]), .55),
        (np.array([2., 0, -1, 1]), -.65),
    )

    for xi, l in all_tests:
        f, p, direction = linesearch_powell(func, p0, xi,
                                            fval=fval, tol=1e-5)
        assert_allclose(f, func(l * xi), atol=1e-6)
        assert_allclose(p, l * xi, atol=1e-6)
        assert_allclose(direction, l * xi, atol=1e-6)

        f, p, direction = linesearch_powell(func, p0, xi, tol=1e-5,
                                            lower_bound=lower_bound,
                                            upper_bound=upper_bound,
                                            fval=fval)
        assert_allclose(f, func(l * xi), atol=1e-6)
        assert_allclose(p, l * xi, atol=1e-6)
        assert_allclose(direction, l * xi, atol=1e-6)

