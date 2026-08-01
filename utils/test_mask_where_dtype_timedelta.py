
def test_mask_where_dtype_timedelta():
    # https://github.com/pandas-dev/pandas/issues/39548
    df = DataFrame([Timedelta(i, unit="D") for i in range(5)])

    expected = DataFrame(np.full(5, np.nan, dtype="timedelta64[s]"))
    tm.assert_frame_equal(df.mask(df.notna()), expected)

    expected = DataFrame(
        [np.nan, np.nan, np.nan, Timedelta("3 day"), Timedelta("4 day")],
        dtype="m8[s]",
    )
    result = df.where(df > Timedelta(2, unit="D"))
    tm.assert_frame_equal(result, expected)

