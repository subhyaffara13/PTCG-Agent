
def test_nuiscance_columns():
    # GH 15015
    df = DataFrame(
        {
            "A": [1, 2, 3],
            "B": [1.0, 2.0, 3.0],
            "C": ["foo", "bar", "baz"],
            "D": date_range("20130101", periods=3),
        }
    )

    result = df.agg("min")
    expected = Series([1, 1.0, "bar", Timestamp("20130101")], index=df.columns)
    tm.assert_series_equal(result, expected)

    result = df.agg(["min"])
    expected = DataFrame(
        [[1, 1.0, "bar", Timestamp("20130101")]],
        index=["min"],
        columns=df.columns,
    )
    tm.assert_frame_equal(result, expected)

    msg = "does not support operation"
    with pytest.raises(TypeError, match=msg):
        df.agg("sum")

    result = df[["A", "B", "C"]].agg("sum")
    expected = Series([6, 6.0, "foobarbaz"], index=["A", "B", "C"])
    tm.assert_series_equal(result, expected)

    msg = "does not support operation"
    with pytest.raises(TypeError, match=msg):
        df.agg(["sum"])

