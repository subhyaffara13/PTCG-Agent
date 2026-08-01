
def test_cython_median():
    arr = np.random.default_rng(2).standard_normal(1000)
    arr[::2] = np.nan
    df = DataFrame(arr)

    labels = np.random.default_rng(2).integers(0, 50, size=1000).astype(float)
    labels[::17] = np.nan

    result = df.groupby(labels).median()
    exp = df.groupby(labels).agg(np.nanmedian)
    tm.assert_frame_equal(result, exp)

    df = DataFrame(np.random.default_rng(2).standard_normal((1000, 5)))
    rs = df.groupby(labels).agg(np.median)
    xp = df.groupby(labels).median()
    tm.assert_frame_equal(rs, xp)

