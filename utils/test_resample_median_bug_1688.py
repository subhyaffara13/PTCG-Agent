
def test_resample_median_bug_1688(dtype, unit):
    # GH#55958
    dti = DatetimeIndex(
        [datetime(2012, 1, 1, 0, 0, 0), datetime(2012, 1, 1, 0, 5, 0)]
    ).as_unit(unit)
    df = DataFrame(
        [1, 2],
        index=dti,
        dtype=dtype,
    )

    result = df.resample("min").apply(lambda x: x.mean())
    exp = df.asfreq("min")
    tm.assert_frame_equal(result, exp)

    result = df.resample("min").median()
    exp = df.asfreq("min")
    tm.assert_frame_equal(result, exp)

