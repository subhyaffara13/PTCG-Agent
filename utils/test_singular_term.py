
def test_singular_term():
    x = np.linspace(0, 1, 10)
    x_test = np.linspace(0.05, 1, 100)
    y = np.empty((2, 10))
    y[0] = (3/4)**0.5
    y[1] = 1e-4
    S = np.array([[0, 0], [0, -2]])

    for fun_jac in [None, emden_fun_jac]:
        for bc_jac in [None, emden_bc_jac]:
            sol = solve_bvp(emden_fun, emden_bc, x, y, S=S, fun_jac=fun_jac,
                            bc_jac=bc_jac)

            assert_equal(sol.status, 0)
            assert_(sol.success)

            assert_equal(sol.x.size, 10)

            sol_test = sol.sol(x_test)
            assert_allclose(sol_test[0], emden_sol(x_test), atol=1e-5)

            f_test = emden_fun(x_test, sol_test) + S.dot(sol_test) / x_test
            r = sol.sol(x_test, 1) - f_test
            rel_res = r / (1 + np.abs(f_test))
            norm_res = np.sum(rel_res ** 2, axis=0) ** 0.5

            assert_(np.all(norm_res < 1e-3))
            assert_allclose(sol.sol(sol.x), sol.y, rtol=1e-10, atol=1e-10)
            assert_allclose(sol.sol(sol.x, 1), sol.yp, rtol=1e-10, atol=1e-10)

