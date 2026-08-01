
def test_vector_constraints():
    # test that fmin_cobyla and minimize can take a combination
    # of constraints, some returning a number and others an array
    def fun(x):
        return (x[0] - 1)**2 + (x[1] - 2.5)**2

    def fmin(x):
        return fun(x) - 1

    def cons1(x):
        a = np.array([[1, -2, 2], [-1, -2, 6], [-1, 2, 2]])
        return np.array([a[i, 0] * x[0] + a[i, 1] * x[1] +
                         a[i, 2] for i in range(len(a))])

    def cons2(x):
        return x     # identity, acts as bounds x > 0

    x0 = np.array([2, 0])
    cons_list = [fun, cons1, cons2]

    xsol = [1.4, 1.7]
    fsol = 0.8

    # testing fmin_cobyla
    sol = fmin_cobyla(fun, x0, cons_list, rhoend=1e-5)
    assert_allclose(sol, xsol, atol=1e-4)

    sol = fmin_cobyla(fun, x0, fmin, rhoend=1e-5)
    assert_allclose(fun(sol), 1, atol=1e-4)

    # testing minimize
    constraints = [{'type': 'ineq', 'fun': cons} for cons in cons_list]
    sol = minimize(fun, x0, constraints=constraints, tol=1e-5)
    assert_allclose(sol.x, xsol, atol=1e-4)
    assert sol.success, sol.message
    assert_allclose(sol.fun, fsol, atol=1e-4)

    constraints = {'type': 'ineq', 'fun': fmin}
    sol = minimize(fun, x0, constraints=constraints, tol=1e-5)
    assert_allclose(sol.fun, 1, atol=1e-4)

