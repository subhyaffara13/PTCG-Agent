
def test_cython_transform_series(op, args, targop):
    # GH 4095
    s = Series(np.random.default_rng(2).standard_normal(1000))
    s_missing = s.copy()
    s_missing.iloc[2:10] = np.nan
    labels = np.random.default_rng(2).integers(0, 50, size=1000).astype(float)

    # series
    for data in [s, s_missing]:
        # print(data.head())
        expected = data.groupby(labels).transform(targop)

        tm.assert_series_equal(expected, data.groupby(labels).transform(op, *args))
        tm.assert_series_equal(expected, getattr(data.groupby(labels), op)(*args))

