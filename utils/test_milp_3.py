
def test_milp_3():
    # solve MIP with inequality constraints and all integer constraints
    # source: https://en.wikipedia.org/wiki/Integer_programming#Example
    c = [0, -1]
    A = [[-1, 1], [3, 2], [2, 3]]
    b_u = [1, 12, 12]
    b_l = np.full_like(b_u, -np.inf, dtype=np.float64)
    constraints = LinearConstraint(A, b_l, b_u)

    integrality = np.ones_like(c)

    # solve original problem
    res = milp(c=c, constraints=constraints, integrality=integrality)
    assert_allclose(res.fun, -2)
    # two optimal solutions possible, just need one of them
    assert np.allclose(res.x, [1, 2]) or np.allclose(res.x, [2, 2])

    # solve relaxed problem
    res = milp(c=c, constraints=constraints)
    assert_allclose(res.fun, -2.8)
    assert_allclose(res.x, [1.8, 2.8])

