
def test_value_counts_integer_columns():
    # GH#55627
    df = DataFrame({1: ["a", "a", "a"], 2: ["a", "a", "d"], 3: ["a", "b", "c"]})
    gp = df.groupby([1, 2], as_index=False, sort=False)
    result = gp[3].value_counts()
    expected = DataFrame(
        {1: ["a", "a", "a"], 2: ["a", "a", "d"], 3: ["a", "b", "c"], "count": 1}
    )
    tm.assert_frame_equal(result, expected)

