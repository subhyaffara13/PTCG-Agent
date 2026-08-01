
def test_entr():
    def xfunc(x):
        if x < 0:
            return -np.inf
        else:
            return -special.xlogy(x, x)
    values = (0, 0.5, 1.0, np.inf)
    signs = [-1, 1]
    arr = []
    for sgn, v in itertools.product(signs, values):
        arr.append(sgn * v)
    z = np.array(arr, dtype=float)
    w = np.vectorize(xfunc, otypes=[np.float64])(z)
    assert_func_equal(special.entr, w, z, rtol=1e-13, atol=1e-13)

