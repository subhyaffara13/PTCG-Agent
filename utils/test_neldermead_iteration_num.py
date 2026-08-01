
def test_neldermead_iteration_num():
    x0 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])
    res = optimize._minimize._minimize_neldermead(optimize.rosen, x0,
                                                  xatol=1e-8)
    assert res.nit <= 339

