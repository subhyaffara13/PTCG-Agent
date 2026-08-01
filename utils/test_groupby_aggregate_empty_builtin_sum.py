
def test_groupby_aggregate_empty_builtin_sum():
    df = DataFrame(columns=["Group", "Data"])
    result = df.groupby(["Group"], as_index=False)["Data"].agg("sum")
    expected = DataFrame(columns=["Group", "Data"])
    tm.assert_frame_equal(result, expected)

