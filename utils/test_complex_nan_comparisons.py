
def test_complex_nan_comparisons():
    nans = [complex(np.nan, 0), complex(0, np.nan), complex(np.nan, np.nan)]
    fins = [complex(1, 0), complex(-1, 0), complex(0, 1), complex(0, -1),
            complex(1, 1), complex(-1, -1), complex(0, 0)]

    with np.errstate(invalid='ignore'):
        for x in nans + fins:
            x = np.array([x])
            for y in nans + fins:
                y = np.array([y])

                if np.isfinite(x) and np.isfinite(y):
                    continue

                assert_equal(x < y, False, err_msg=f"{x!r} < {y!r}")
                assert_equal(x > y, False, err_msg=f"{x!r} > {y!r}")
                assert_equal(x <= y, False, err_msg=f"{x!r} <= {y!r}")
                assert_equal(x >= y, False, err_msg=f"{x!r} >= {y!r}")
                assert_equal(x == y, False, err_msg=f"{x!r} == {y!r}")

