
def test_big_problem():
    n = 30
    x = np.linspace(0, 1, 5)
    y = np.zeros((2 * n, x.size))
    sol = solve_bvp(big_fun, big_bc, x, y)

    assert_equal(sol.status, 0)
    assert_(sol.success)

    sol_test = sol.sol(x)

    assert_allclose(sol_test[0], big_sol(x, n))

    f_test = big_fun(x, sol_test)
    r = sol.sol(x, 1) - f_test
    rel_res = r / (1 + np.abs(f_test))
    norm_res = np.sum(np.real(rel_res * np.conj(rel_res)), axis=0) ** 0.5
    assert_(np.all(norm_res < 1e-3))

    assert_(np.all(sol.rms_residuals < 1e-3))
    assert_allclose(sol.sol(sol.x), sol.y, rtol=1e-10, atol=1e-10)
    assert_allclose(sol.sol(sol.x, 1), sol.yp, rtol=1e-10, atol=1e-10)

