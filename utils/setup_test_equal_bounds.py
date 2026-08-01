
def setup_test_equal_bounds():
    # the success of test_equal_bounds depends on the exact seed
    rng = np.random.default_rng(12223)
    x0 = rng.random(4)
    lb = np.array([0, 2, -1, -1.0])
    ub = np.array([3, 2, 2, -1.0])
    i_eb = (lb == ub)

    def check_x(x, check_size=True, check_values=True):
        if check_size:
            assert x.size == 4
        if check_values:
            assert_allclose(x[i_eb], lb[i_eb])

    def func(x):
        check_x(x)
        return optimize.rosen(x)

    def grad(x):
        check_x(x)
        return optimize.rosen_der(x)

    def callback(x, *args):
        check_x(x)

    def callback2(intermediate_result):
        assert isinstance(intermediate_result, OptimizeResult)
        check_x(intermediate_result.x)

    def constraint1(x):
        check_x(x, check_values=False)
        return x[0:1] - 1

    def jacobian1(x):
        check_x(x, check_values=False)
        dc = np.zeros_like(x)
        dc[0] = 1
        return dc

    def constraint2(x):
        check_x(x, check_values=False)
        return x[2:3] - 0.5

    def jacobian2(x):
        check_x(x, check_values=False)
        dc = np.zeros_like(x)
        dc[2] = 1
        return dc

    c1a = NonlinearConstraint(constraint1, -np.inf, 0)
    c1b = NonlinearConstraint(constraint1, -np.inf, 0, jacobian1)
    c2a = NonlinearConstraint(constraint2, -np.inf, 0)
    c2b = NonlinearConstraint(constraint2, -np.inf, 0, jacobian2)

    # test using the three methods that accept bounds, use derivatives, and
    # have some trouble when bounds fix variables
    methods = ('L-BFGS-B', 'SLSQP', 'TNC')

    # test w/out gradient, w/ gradient, and w/ combined objective/gradient
    kwds = ({"fun": func, "jac": False},
            {"fun": func, "jac": grad},
            {"fun": (lambda x: (func(x), grad(x))),
             "jac": True})

    # test with both old- and new-style bounds
    bound_types = (lambda lb, ub: list(zip(lb, ub)),
                   Bounds)

    # Test for many combinations of constraints w/ and w/out jacobian
    # Pairs in format: (test constraints, reference constraints)
    # (always use analytical jacobian in reference)
    constraints = ((None, None), ([], []),
                   (c1a, c1b), (c2b, c2b),
                   ([c1b], [c1b]), ([c2a], [c2b]),
                   ([c1a, c2a], [c1b, c2b]),
                   ([c1a, c2b], [c1b, c2b]),
                   ([c1b, c2b], [c1b, c2b]))

    # test with and without callback function
    callbacks = (None, callback, callback2)

    data = {"methods": methods, "kwds": kwds, "bound_types": bound_types,
            "constraints": constraints, "callbacks": callbacks,
            "lb": lb, "ub": ub, "x0": x0, "i_eb": i_eb}

    return data

