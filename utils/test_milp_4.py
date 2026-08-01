
def test_milp_4():
    # solve MIP with inequality constraints and only one integer constraint
    # source: https://www.mathworks.com/help/optim/ug/intlinprog.html
    c = [8, 1]
    integrality = [0, 1]
    A = [[1, 2], [-4, -1], [2, 1]]
    b_l = [-14, -np.inf, -np.inf]
    b_u = [np.inf, -33, 20]
    constraints = LinearConstraint(A, b_l, b_u)
    bounds = Bounds(-np.inf, np.inf)

    res = milp(c, integrality=integrality, bounds=bounds,
               constraints=constraints)
    assert_allclose(res.fun, 59)
    assert_allclose(res.x, [6.5, 7])

