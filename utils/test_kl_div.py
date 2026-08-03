import itertools

def test_kl_div():
    def xfunc(x, y):
        if x < 0 or y < 0 or (y == 0 and x != 0):
            # extension of natural domain to preserve convexity
            return np.inf
        elif np.isposinf(x) or np.isposinf(y):
            # limits within the natural domain
            return np.inf
        elif x == 0:
            return y
        else:
            return special.xlogy(x, x/y) - x + y
    values = (0, 0.5, 1.0)
    signs = [-1, 1]
    arr = []
    for sgna, va, sgnb, vb in itertools.product(signs, values, signs, values):
        arr.append((sgna*va, sgnb*vb))
    z = np.array(arr, dtype=float)
    w = np.vectorize(xfunc, otypes=[np.float64])(z[:,0], z[:,1])
    assert_func_equal(special.kl_div, w, z, rtol=1e-13, atol=1e-13)

