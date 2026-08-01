
def test_huber():
    assert_equal(special.huber(-1, 1.5), np.inf)
    assert_allclose(special.huber(2, 1.5), 0.5 * np.square(1.5))
    assert_allclose(special.huber(2, 2.5), 2 * (2.5 - 0.5 * 2))

    def xfunc(delta, r):
        if delta < 0:
            return np.inf
        elif np.abs(r) < delta:
            return 0.5 * np.square(r)
        else:
            return delta * (np.abs(r) - 0.5 * delta)

    z = np.random.randn(10, 2)
    w = np.vectorize(xfunc, otypes=[np.float64])(z[:,0], z[:,1])
    assert_func_equal(special.huber, w, z, rtol=1e-13, atol=1e-13)

