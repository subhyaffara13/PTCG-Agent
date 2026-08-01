
def test_fp32_gh12991():
    # checks that smaller FP sizes can be used in least_squares
    # this is the minimum working example reported for gh12991
    rng = np.random.default_rng(1978)

    x = np.linspace(0, 1, 100, dtype=np.float32)
    y = rng.random(size=100, dtype=np.float32)

    # changed in gh21872. These functions should've been working in fp32 to force
    # approx_derivative to work in fp32. One of the initial steps in least_squares
    # is to force x0 (p) to be a float, meaning that the output of func and err would
    # be in float64, unless forced to be in float32
    def func(p, x):
        return (p[0] + p[1] * x).astype(np.float32)

    def err(p, x, y):
        return (func(p, x) - y).astype(np.float32)

    def mse(p, x, y):
        return np.sum(err(p, x, y)**2)

    res = least_squares(err, [-1.0, -1.0], args=(x, y))
    # previously the initial jacobian calculated for this would be all 0
    # and the minimize would terminate immediately, with nfev=1, would
    # report a successful minimization (it shouldn't have done), but be
    # unchanged from the initial solution.
    # It was terminating early because the underlying approx_derivative
    # used a step size for FP64 when the working space was FP32.
    assert res.nfev > 2
    # compare output to solver that doesn't use derivatives
    res2 = minimize(
        mse,
        [-1.0, 1.0],
        method='cobyqa',
        args=(x, y),
        options={'final_tr_radius': 1e-6}
    )
    assert_allclose(res.x, res2.x, atol=9e-5)

