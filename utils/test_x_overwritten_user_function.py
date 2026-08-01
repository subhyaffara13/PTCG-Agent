
def test_x_overwritten_user_function():
    # if the user overwrites the x-array in the user function it's likely
    # that the minimizer stops working properly.
    # gh13740
    def fquad(x):
        a = np.arange(np.size(x))
        x -= a
        x *= x
        return np.sum(x)

    def fquad_jac(x):
        a = np.arange(np.size(x))
        x *= 2
        x -= 2 * a
        return x

    def fquad_hess(x):
        return np.eye(np.size(x)) * 2.0

    meth_jac = [
        'newton-cg', 'dogleg', 'trust-ncg', 'trust-exact',
        'trust-krylov', 'trust-constr'
    ]
    meth_hess = [
        'dogleg', 'trust-ncg', 'trust-exact', 'trust-krylov', 'trust-constr'
    ]

    x0 = np.ones(5) * 1.5

    for meth in MINIMIZE_METHODS:
        jac = None
        hess = None
        if meth in meth_jac:
            jac = fquad_jac
        if meth in meth_hess:
            hess = fquad_hess
        res = optimize.minimize(fquad, x0, method=meth, jac=jac, hess=hess)
        assert_allclose(res.x, np.arange(np.size(x0)), atol=2e-4)

