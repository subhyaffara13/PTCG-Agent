
def test_neldermead_xatol_fatol():
    # gh4484
    # test we can call with fatol, xatol specified
    def func(x):
        return x[0] ** 2 + x[1] ** 2

    optimize._minimize._minimize_neldermead(func, [1, 1], maxiter=2,
                                            xatol=1e-3, fatol=1e-3)

