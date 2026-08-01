
def test_milp_5():
    # solve MIP with inequality and equality constraints
    # source: https://www.mathworks.com/help/optim/ug/intlinprog.html
    c = [-3, -2, -1]
    integrality = [0, 0, 1]
    lb = [0, 0, 0]
    ub = [np.inf, np.inf, 1]
    bounds = Bounds(lb, ub)
    A = [[1, 1, 1], [4, 2, 1]]
    b_l = [-np.inf, 12]
    b_u = [7, 12]
    constraints = LinearConstraint(A, b_l, b_u)

    res = milp(c, integrality=integrality, bounds=bounds,
               constraints=constraints)
    # there are multiple solutions
    assert_allclose(res.fun, -12)

