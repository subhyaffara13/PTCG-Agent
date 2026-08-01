
def test_linesearch_powell_bounded():
    # helper function in optimize.py, not a public function.
    linesearch_powell = optimize._optimize._linesearch_powell
    # args are func, p, xi, fval, lower_bound=None, upper_bound=None, tol=1e-3
    # returns new_fval, p+direction, direction
    def func(x):
        return np.sum((x - np.array([-1.0, 2.0, 1.5, -0.4])) ** 2)
    p0 = np.array([0., 0, 0, 0])
    fval = func(p0)

    # first choose bounds such that the same tests from
    # test_linesearch_powell should pass.
    lower_bound = np.array([-2.]*4)
    upper_bound = np.array([2.]*4)

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
        f, p, direction = linesearch_powell(func, p0, xi, tol=1e-5,
                                            lower_bound=lower_bound,
                                            upper_bound=upper_bound,
                                            fval=fval)
        assert_allclose(f, func(l * xi), atol=1e-6)
        assert_allclose(p, l * xi, atol=1e-6)
        assert_allclose(direction, l * xi, atol=1e-6)

    # now choose bounds such that unbounded vs bounded gives different results
    lower_bound = np.array([-.3]*3 + [-1])
    upper_bound = np.array([.45]*3 + [.9])

    all_tests = (
        (np.array([1., 0, 0, 0]), -.3),
        (np.array([0., 1, 0, 0]), .45),
        (np.array([0., 0, 1, 0]), .45),
        (np.array([0., 0, 0, 1]), -.4),
        (np.array([-1., 0, 1, 0]), .3),
        (np.array([0., 0, 1, 1]), .45),
        (np.array([2., 0, -1, 1]), -.15),
    )

    for xi, l in all_tests:
        f, p, direction = linesearch_powell(func, p0, xi, tol=1e-5,
                                            lower_bound=lower_bound,
                                            upper_bound=upper_bound,
                                            fval=fval)
        assert_allclose(f, func(l * xi), atol=1e-6)
        assert_allclose(p, l * xi, atol=1e-6)
        assert_allclose(direction, l * xi, atol=1e-6)

    # now choose as above but start outside the bounds
    p0 = np.array([-1., 0, 0, 2])
    fval = func(p0)

    all_tests = (
        (np.array([1., 0, 0, 0]), .7),
        (np.array([0., 1, 0, 0]), .45),
        (np.array([0., 0, 1, 0]), .45),
        (np.array([0., 0, 0, 1]), -2.4),
    )

    for xi, l in all_tests:
        f, p, direction = linesearch_powell(func, p0, xi, tol=1e-5,
                                            lower_bound=lower_bound,
                                            upper_bound=upper_bound,
                                            fval=fval)
        assert_allclose(f, func(p0 + l * xi), atol=1e-6)
        assert_allclose(p, p0 + l * xi, atol=1e-6)
        assert_allclose(direction, l * xi, atol=1e-6)

    # now mix in inf
    p0 = np.array([0., 0, 0, 0])
    fval = func(p0)

    # now choose bounds that mix inf
    lower_bound = np.array([-.3, -np.inf, -np.inf, -1])
    upper_bound = np.array([np.inf, .45, np.inf, .9])

    all_tests = (
        (np.array([1., 0, 0, 0]), -.3),
        (np.array([0., 1, 0, 0]), .45),
        (np.array([0., 0, 1, 0]), 1.5),
        (np.array([0., 0, 0, 1]), -.4),
        (np.array([-1., 0, 1, 0]), .3),
        (np.array([0., 0, 1, 1]), .55),
        (np.array([2., 0, -1, 1]), -.15),
    )

    for xi, l in all_tests:
        f, p, direction = linesearch_powell(func, p0, xi, tol=1e-5,
                                            lower_bound=lower_bound,
                                            upper_bound=upper_bound,
                                            fval=fval)
        assert_allclose(f, func(l * xi), atol=1e-6)
        assert_allclose(p, l * xi, atol=1e-6)
        assert_allclose(direction, l * xi, atol=1e-6)

    # now choose as above but start outside the bounds
    p0 = np.array([-1., 0, 0, 2])
    fval = func(p0)

    all_tests = (
        (np.array([1., 0, 0, 0]), .7),
        (np.array([0., 1, 0, 0]), .45),
        (np.array([0., 0, 1, 0]), 1.5),
        (np.array([0., 0, 0, 1]), -2.4),
    )

    for xi, l in all_tests:
        f, p, direction = linesearch_powell(func, p0, xi, tol=1e-5,
                                            lower_bound=lower_bound,
                                            upper_bound=upper_bound,
                                            fval=fval)
        assert_allclose(f, func(p0 + l * xi), atol=1e-6)
        assert_allclose(p, p0 + l * xi, atol=1e-6)
        assert_allclose(direction, l * xi, atol=1e-6)

