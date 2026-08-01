
def test_powell_output():
    funs = [rosen, lambda x: np.array(rosen(x)), lambda x: np.array([rosen(x)])]
    for fun in funs:
        res = optimize.minimize(fun, x0=[0.6, 20], method='Powell')
        assert np.isscalar(res.fun)

