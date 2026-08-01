
def test_npymath_complex(fun, npfun, x, y, test_dtype):
    # Smoketest npymath functions
    z = test_dtype(complex(x, y))
    with np.errstate(invalid='ignore'):
        # Fallback implementations may emit a warning for +-inf (see gh-24876):
        #     RuntimeWarning: invalid value encountered in absolute
        got = fun(z)
        expected = npfun(z)
        assert_allclose(got, expected)

