
def test_xlog1py():
    def xfunc(x, y):
        with np.errstate(invalid='ignore'):
            if x == 0 and not np.isnan(y):
                return x
            else:
                return x * np.log1p(y)

    z1 = np.asarray([(0,0), (0, np.nan), (0, np.inf), (1.0, 2.0),
                     (1, 1e-30)], dtype=float)
    w1 = np.vectorize(xfunc)(z1[:,0], z1[:,1])
    assert_func_equal(special.xlog1py, w1, z1, rtol=1e-13, atol=1e-13)

