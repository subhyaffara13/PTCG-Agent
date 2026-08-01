
def test_resample_across_dst():
    # The test resamples a DatetimeIndex with values before and after a
    # DST change
    # Issue: 14682

    # The DatetimeIndex we will start with
    # (note that DST happens at 03:00+02:00 -> 02:00+01:00)
    # 2016-10-30 02:23:00+02:00, 2016-10-30 02:23:00+01:00
    df1 = DataFrame([1477786980, 1477790580], columns=["ts"])
    dti1 = DatetimeIndex(
        pd.to_datetime(df1.ts, unit="s")
        .dt.tz_localize("UTC")
        .dt.tz_convert("Europe/Madrid")
    )

    # The expected DatetimeIndex after resampling.
    # 2016-10-30 02:00:00+02:00, 2016-10-30 02:00:00+01:00
    df2 = DataFrame([1477785600, 1477789200], columns=["ts"])
    dti2 = DatetimeIndex(
        pd.to_datetime(df2.ts, unit="s")
        .dt.tz_localize("UTC")
        .dt.tz_convert("Europe/Madrid"),
        freq="h",
    )
    df = DataFrame([5, 5], index=dti1)

    result = df.resample(rule="h").sum()
    expected = DataFrame([5, 5], index=dti2)

    tm.assert_frame_equal(result, expected)

