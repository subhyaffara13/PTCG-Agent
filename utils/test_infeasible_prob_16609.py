
def test_infeasible_prob_16609():
    # Ensure presolve does not mark trivially infeasible problems
    # as Optimal -- see gh-16609
    c = [1.0, 0.0]
    integrality = [0, 1]

    lb = [0, -np.inf]
    ub = [np.inf, np.inf]
    bounds = Bounds(lb, ub)

    A_eq = [[0.0, 1.0]]
    b_eq = [0.5]
    constraints = LinearConstraint(A_eq, b_eq, b_eq)

    res = milp(c, integrality=integrality, bounds=bounds,
               constraints=constraints)
    np.testing.assert_equal(res.status, 2)

