
def test_failures():
    x = np.linspace(0, 1, 2)
    y = np.zeros((2, x.size))
    res = solve_bvp(exp_fun, exp_bc, x, y, tol=1e-5, max_nodes=5)
    assert_equal(res.status, 1)
    assert_(not res.success)

    x = np.linspace(0, 1, 5)
    y = np.zeros((2, x.size))
    res = solve_bvp(undefined_fun, undefined_bc, x, y)
    assert_equal(res.status, 2)
    assert_(not res.success)

