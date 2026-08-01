
def test_with_params():
    x = np.linspace(0, np.pi, 5)
    x_test = np.linspace(0, np.pi, 100)
    y = np.ones((2, x.shape[0]))

    for fun_jac in [None, sl_fun_jac]:
        for bc_jac in [None, sl_bc_jac]:
            sol = solve_bvp(sl_fun, sl_bc, x, y, p=[0.5], fun_jac=fun_jac,
                            bc_jac=bc_jac)

            assert_equal(sol.status, 0)
            assert_(sol.success)

            assert_(sol.x.size < 10)

            assert_allclose(sol.p, [1], rtol=1e-4)

            sol_test = sol.sol(x_test)

            assert_allclose(sol_test[0], sl_sol(x_test, [1]),
                            rtol=1e-4, atol=1e-4)

            f_test = sl_fun(x_test, sol_test, [1])
            r = sol.sol(x_test, 1) - f_test
            rel_res = r / (1 + np.abs(f_test))
            norm_res = np.sum(rel_res ** 2, axis=0) ** 0.5
            assert_(np.all(norm_res < 1e-3))

            assert_(np.all(sol.rms_residuals < 1e-3))
            assert_allclose(sol.sol(sol.x), sol.y, rtol=1e-10, atol=1e-10)
            assert_allclose(sol.sol(sol.x, 1), sol.yp, rtol=1e-10, atol=1e-10)

