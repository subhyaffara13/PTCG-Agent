
def test_start_stop_fixed(temp_hdfstore):
    # fixed, GH 8287
    store = temp_hdfstore
    df = DataFrame(
        {
            "A": np.random.default_rng(2).random(20),
            "B": np.random.default_rng(2).random(20),
        },
        index=date_range("20130101", periods=20),
    )
    store.put("df", df)

    result = store.select("df", start=0, stop=5)
    expected = df.iloc[0:5, :]
    tm.assert_frame_equal(result, expected)

    result = store.select("df", start=5, stop=10)
    expected = df.iloc[5:10, :]
    tm.assert_frame_equal(result, expected)

    # out of range
    result = store.select("df", start=30, stop=40)
    expected = df.iloc[30:40, :]
    tm.assert_frame_equal(result, expected)

    # series
    s = df.A
    store.put("s", s)
    result = store.select("s", start=0, stop=5)
    expected = s.iloc[0:5]
    tm.assert_series_equal(result, expected)

    result = store.select("s", start=5, stop=10)
    expected = s.iloc[5:10]
    tm.assert_series_equal(result, expected)

    # sparse; not implemented
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )
    df.iloc[3:5, 1:3] = np.nan
    df.iloc[8:10, -2] = np.nan

