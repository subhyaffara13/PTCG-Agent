
def test_pseudo_huber():
    def xfunc(delta, r):
        if delta < 0:
            return np.inf
        elif (not delta) or (not r):
            return 0
        else:
            return delta**2 * (np.sqrt(1 + (r/delta)**2) - 1)

    z = np.array(np.random.randn(10, 2).tolist() + [[0, 0.5], [0.5, 0]])
    w = np.vectorize(xfunc, otypes=[np.float64])(z[:,0], z[:,1])
    assert_func_equal(special.pseudo_huber, w, z, rtol=1e-13, atol=1e-13)

