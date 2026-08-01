
def test_powell_limits():
    # gh15342 - powell was going outside bounds for some function evaluations.
    bounds = optimize.Bounds([0, 0], [0.6, 20])

    def fun(x):
        a, b = x
        assert (x >= bounds.lb).all() and (x <= bounds.ub).all()
        return a ** 2 + b ** 2

    optimize.minimize(fun, x0=[0.6, 20], method='Powell', bounds=bounds)

    # Another test from the original report - gh-13411
    bounds = optimize.Bounds(lb=[0,], ub=[1,], keep_feasible=[True,])

    def func(x):
        assert x >= 0 and x <= 1
        return np.exp(x)

    optimize.minimize(fun=func, x0=[0.5], method='powell', bounds=bounds)

