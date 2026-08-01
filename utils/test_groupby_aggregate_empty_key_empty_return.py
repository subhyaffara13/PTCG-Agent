
def test_groupby_aggregate_empty_key_empty_return():
    # GH: 32580 Check if everything works, when return is empty
    df = DataFrame({"a": [1, 1, 2], "b": [1, 2, 3], "c": [1, 2, 4]})
    result = df.groupby("a").agg({"b": []})
    expected = DataFrame(columns=MultiIndex(levels=[["b"], []], codes=[[], []]))
    tm.assert_frame_equal(result, expected)

