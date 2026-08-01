
def test_ewm_alpha():
    # GH 10789
    arr = np.random.default_rng(2).standard_normal(100)
    locs = np.arange(20, 40)
    arr[locs] = np.nan

    s = Series(arr)
    a = s.ewm(alpha=0.61722699889169674).mean()
    b = s.ewm(com=0.62014947789973052).mean()
    c = s.ewm(span=2.240298955799461).mean()
    d = s.ewm(halflife=0.721792864318).mean()
    tm.assert_series_equal(a, b)
    tm.assert_series_equal(a, c)
    tm.assert_series_equal(a, d)

