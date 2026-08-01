
def test_line_for_search():
    # _line_for_search is only used in _linesearch_powell, which is also
    # tested below. Thus there are more tests of _line_for_search in the
    # test_linesearch_powell_bounded function.

    line_for_search = optimize._optimize._line_for_search
    # args are x0, alpha, lower_bound, upper_bound
    # returns lmin, lmax

    lower_bound = np.array([-5.3, -1, -1.5, -3])
    upper_bound = np.array([1.9, 1, 2.8, 3])

    # test when starting in the bounds
    x0 = np.array([0., 0, 0, 0])
    # and when starting outside of the bounds
    x1 = np.array([0., 2, -3, 0])

    all_tests = (
        (x0, np.array([1., 0, 0, 0]), -5.3, 1.9),
        (x0, np.array([0., 1, 0, 0]), -1, 1),
        (x0, np.array([0., 0, 1, 0]), -1.5, 2.8),
        (x0, np.array([0., 0, 0, 1]), -3, 3),
        (x0, np.array([1., 1, 0, 0]), -1, 1),
        (x0, np.array([1., 0, -1, 2]), -1.5, 1.5),
        (x0, np.array([2., 0, -1, 2]), -1.5, 0.95),
        (x1, np.array([1., 0, 0, 0]), -5.3, 1.9),
        (x1, np.array([0., 1, 0, 0]), -3, -1),
        (x1, np.array([0., 0, 1, 0]), 1.5, 5.8),
        (x1, np.array([0., 0, 0, 1]), -3, 3),
        (x1, np.array([1., 1, 0, 0]), -3, -1),
        (x1, np.array([1., 0, -1, 0]), -5.3, -1.5),
    )

    for x, alpha, lmin, lmax in all_tests:
        mi, ma = line_for_search(x, alpha, lower_bound, upper_bound)
        assert_allclose(mi, lmin, atol=1e-6)
        assert_allclose(ma, lmax, atol=1e-6)

    # now with infinite bounds
    lower_bound = np.array([-np.inf, -1, -np.inf, -3])
    upper_bound = np.array([np.inf, 1, 2.8, np.inf])

    all_tests = (
        (x0, np.array([1., 0, 0, 0]), -np.inf, np.inf),
        (x0, np.array([0., 1, 0, 0]), -1, 1),
        (x0, np.array([0., 0, 1, 0]), -np.inf, 2.8),
        (x0, np.array([0., 0, 0, 1]), -3, np.inf),
        (x0, np.array([1., 1, 0, 0]), -1, 1),
        (x0, np.array([1., 0, -1, 2]), -1.5, np.inf),
        (x1, np.array([1., 0, 0, 0]), -np.inf, np.inf),
        (x1, np.array([0., 1, 0, 0]), -3, -1),
        (x1, np.array([0., 0, 1, 0]), -np.inf, 5.8),
        (x1, np.array([0., 0, 0, 1]), -3, np.inf),
        (x1, np.array([1., 1, 0, 0]), -3, -1),
        (x1, np.array([1., 0, -1, 0]), -5.8, np.inf),
    )

    for x, alpha, lmin, lmax in all_tests:
        mi, ma = line_for_search(x, alpha, lower_bound, upper_bound)
        assert_allclose(mi, lmin, atol=1e-6)
        assert_allclose(ma, lmax, atol=1e-6)

