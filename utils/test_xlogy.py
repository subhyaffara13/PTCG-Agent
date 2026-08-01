
def test_xlogy():
    def xfunc(x, y):
        with np.errstate(invalid='ignore'):
            if x == 0 and not np.isnan(y):
                return x
            else:
                return x*np.log(y)

    z1 = np.asarray([(0,0), (0, np.nan), (0, np.inf), (1.0, 2.0)], dtype=float)
    z2 = np.r_[z1, [(0, 1j), (1, 1j)]]

    w1 = np.vectorize(xfunc)(z1[:,0], z1[:,1])
    assert_func_equal(special.xlogy, w1, z1, rtol=1e-13, atol=1e-13)
    w2 = np.vectorize(xfunc)(z2[:,0], z2[:,1])
    assert_func_equal(special.xlogy, w2, z2, rtol=1e-13, atol=1e-13)

