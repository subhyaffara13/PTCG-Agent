
def test_gh11649():
    # trust - constr error when attempting to keep bound constrained solutions
    # feasible. Algorithm attempts to go outside bounds when evaluating finite
    # differences. (don't give objective an analytic gradient)
    bnds = Bounds(lb=[-1, -1], ub=[1, 1], keep_feasible=True)

    def assert_inbounds(x):
        assert np.all(x >= bnds.lb)
        assert np.all(x <= bnds.ub)

    def obj(x):
        assert_inbounds(x)
        return np.exp(x[0])*(4*x[0]**2 + 2*x[1]**2 + 4*x[0]*x[1] + 2*x[1] + 1)

    def nce(x):
        assert_inbounds(x)
        return x[0]**2 + x[1]

    def nce_jac(x):
        return np.array([2*x[0], 1])

    def nci(x):
        assert_inbounds(x)
        return x[0]*x[1]

    x0 = np.array((0.99, -0.99))
    nlcs = [NonlinearConstraint(nci, -10, np.inf),
            NonlinearConstraint(nce, 1, 1, jac=nce_jac)]

    res = minimize(fun=obj, x0=x0, method='trust-constr',
                   bounds=bnds, constraints=nlcs)
    assert_inbounds(res.x)
    assert nlcs[0].lb < nlcs[0].fun(res.x) < nlcs[0].ub

