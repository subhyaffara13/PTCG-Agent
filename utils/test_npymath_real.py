
def test_npymath_real():
    # Smoketest npymath functions
    from numpy._core._multiarray_tests import (
        npy_cosh,
        npy_log10,
        npy_sinh,
        npy_tan,
        npy_tanh,
    )

    funcs = {npy_log10: np.log10,
             npy_cosh: np.cosh,
             npy_sinh: np.sinh,
             npy_tan: np.tan,
             npy_tanh: np.tanh}
    vals = (1, np.inf, -np.inf, np.nan)
    types = (np.float32, np.float64, np.longdouble)

    with np.errstate(all='ignore'):
        for fun, npfun in funcs.items():
            for x, t in itertools.product(vals, types):
                z = t(x)
                got = fun(z)
                expected = npfun(z)
                assert_allclose(got, expected)

