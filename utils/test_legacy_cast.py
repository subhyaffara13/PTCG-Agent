
def test_legacy_cast():
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            "floating point number truncated to an integer",
            RuntimeWarning
        )
        res = sc.bdtrc(np.nan, 1, 0.5)
        assert_(np.isnan(res))

