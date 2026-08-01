
def test_rel_entr():
    def xfunc(x, y):
        if x > 0 and y > 0:
            return special.xlogy(x, x/y)
        elif x == 0 and y >= 0:
            return 0
        else:
            return np.inf
    values = (0, 0.5, 1.0)
    signs = [-1, 1]
    arr = []
    for sgna, va, sgnb, vb in itertools.product(signs, values, signs, values):
        arr.append((sgna*va, sgnb*vb))
    z = np.array(arr, dtype=float)
    w = np.vectorize(xfunc, otypes=[np.float64])(z[:,0], z[:,1])
    assert_func_equal(special.rel_entr, w, z, rtol=1e-13, atol=1e-13)

