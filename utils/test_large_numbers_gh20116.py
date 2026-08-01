
def test_large_numbers_gh20116():
    h = 10 ** 12
    A = np.array([[100.4534, h], [100.4534, -h]])
    b = np.array([h, 0])
    constraints = LinearConstraint(A=A, ub=b)
    bounds = Bounds([0, 0], [1, 1])
    c = np.array([0, 0])
    res = milp(c=c, constraints=constraints, bounds=bounds, integrality=1)
    assert res.status == 0
    assert np.all(A @ res.x < b)

