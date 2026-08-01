
def test_groupby_aggregate_empty_udf():
    def func(x):
        return sum(x)

    df = DataFrame(columns=["Group", "Data"])
    result = df.groupby(["Group"], as_index=False)["Data"].agg(func)
    expected = DataFrame(columns=["Group", "Data"])
    tm.assert_frame_equal(result, expected)

