
def test_resample_apply_product(duplicates, unit):
    # GH 5586
    index = date_range(start="2012-01-31", freq="ME", periods=12).as_unit(unit)

    ts = Series(range(12), index=index)
    df = DataFrame({"A": ts, "B": ts + 2})
    if duplicates:
        df.columns = ["A", "A"]

    result = df.resample("QE").apply(np.prod)
    expected = DataFrame(
        np.array([[0, 24], [60, 210], [336, 720], [990, 1716]], dtype=np.int64),
        index=DatetimeIndex(
            ["2012-03-31", "2012-06-30", "2012-09-30", "2012-12-31"], freq="QE-DEC"
        ).as_unit(unit),
        columns=df.columns,
    )
    tm.assert_frame_equal(result, expected)

