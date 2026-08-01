
def test_result_x_shape_when_len_x_is_one():
    def fun(x):
        return x * x

    def jac(x):
        return 2. * x

    def hess(x):
        return np.array([[2.]])

    methods = ['Nelder-Mead', 'Powell', 'CG', 'BFGS', 'L-BFGS-B', 'TNC',
               'COBYLA', 'COBYQA', 'SLSQP']
    for method in methods:
        res = optimize.minimize(fun, np.array([0.1]), method=method)
        assert res.x.shape == (1,)

    # use jac + hess
    methods = ['trust-constr', 'dogleg', 'trust-ncg', 'trust-exact',
               'trust-krylov', 'Newton-CG']
    for method in methods:
        res = optimize.minimize(fun, np.array([0.1]), method=method, jac=jac,
                                hess=hess)
        assert res.x.shape == (1,)

