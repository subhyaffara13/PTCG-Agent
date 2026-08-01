
def test_milp_timeout_16545(options, msg):
    # Ensure solution is not thrown away if MILP solver times out
    # -- see gh-16545
    rng = np.random.default_rng(5123833489170494244)
    A = rng.integers(0, 5, size=(100, 100))
    b_lb = np.full(100, fill_value=-np.inf)
    b_ub = np.full(100, fill_value=25)
    constraints = LinearConstraint(A, b_lb, b_ub)
    variable_lb = np.zeros(100)
    variable_ub = np.ones(100)
    variable_bounds = Bounds(variable_lb, variable_ub)
    integrality = np.ones(100)
    c_vector = -np.ones(100)
    res = milp(
        c_vector,
        integrality=integrality,
        bounds=variable_bounds,
        constraints=constraints,
        options=options,
    )

    assert res.message.startswith(msg)
    assert res["x"] is not None

    # ensure solution is feasible
    x = res["x"]
    tol = 1e-8  # sometimes needed due to finite numerical precision
    assert np.all(b_lb - tol <= A @ x) and np.all(A @ x <= b_ub + tol)
    assert np.all(variable_lb - tol <= x) and np.all(x <= variable_ub + tol)
    assert np.allclose(x, np.round(x))

