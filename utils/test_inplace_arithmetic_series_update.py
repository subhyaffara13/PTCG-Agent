
def test_inplace_arithmetic_series_update():
    # https://github.com/pandas-dev/pandas/issues/36373
    df = DataFrame({"A": [1, 2, 3]})
    df_orig = df.copy()
    series = df["A"]
    vals = series._values

    series += 1
    assert series._values is not vals
    tm.assert_frame_equal(df, df_orig)

