
def test_resample_timegrouper(dates, unit):
    # GH 7227
    dates = DatetimeIndex(dates).as_unit(unit)
    df = DataFrame({"A": dates, "B": np.arange(len(dates))})
    result = df.set_index("A").resample("ME").count()
    exp_idx = DatetimeIndex(
        ["2014-07-31", "2014-08-31", "2014-09-30", "2014-10-31", "2014-11-30"],
        freq="ME",
        name="A",
    ).as_unit(unit)
    expected = DataFrame({"B": [1, 0, 2, 2, 1]}, index=exp_idx)
    if df["A"].isna().any():
        expected.index = expected.index._with_freq(None)
    tm.assert_frame_equal(result, expected)

    result = df.groupby(Grouper(freq="ME", key="A")).count()
    tm.assert_frame_equal(result, expected)

