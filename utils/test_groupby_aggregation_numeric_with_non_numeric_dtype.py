
def test_groupby_aggregation_numeric_with_non_numeric_dtype():
    # GH #43108
    df = DataFrame(
        {
            "x": [1, 0, 1, 1, 0],
            "y": [Timedelta(i, "days") for i in range(1, 6)],
            "z": list(range(1, 6)),
        }
    )

    expected = DataFrame(
        {"y": [Timedelta(7, "days"), Timedelta(8, "days")], "z": [7, 8]},
        index=Index([0, 1], dtype="int64", name="x"),
    )

    gb = df.groupby(by=["x"])
    result = gb.sum()
    tm.assert_frame_equal(result, expected)

