
def test_groupby_aggregation_non_numeric_dtype():
    # GH #43108
    df = DataFrame(
        [["M", [1]], ["M", [1]], ["W", [10]], ["W", [20]]], columns=["MW", "v"]
    )

    expected = DataFrame(
        {
            "v": [[1, 1], [10, 20]],
        },
        index=Index(["M", "W"], name="MW"),
    )

    gb = df.groupby(by=["MW"])
    result = gb.sum()
    tm.assert_frame_equal(result, expected)

