
def test_resample_integerarray(unit):
    # GH 25580, resample on IntegerArray
    ts = Series(
        range(9),
        index=date_range("1/1/2000", periods=9, freq="min").as_unit(unit),
        dtype="Int64",
    )
    result = ts.resample("3min").sum()
    expected = Series(
        [3, 12, 21],
        index=date_range("1/1/2000", periods=3, freq="3min").as_unit(unit),
        dtype="Int64",
    )
    tm.assert_series_equal(result, expected)

    result = ts.resample("3min").mean()
    expected = Series(
        [1, 4, 7],
        index=date_range("1/1/2000", periods=3, freq="3min").as_unit(unit),
        dtype="Float64",
    )
    tm.assert_series_equal(result, expected)

