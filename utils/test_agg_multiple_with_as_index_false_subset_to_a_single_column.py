
def test_agg_multiple_with_as_index_false_subset_to_a_single_column():
    # GH#50724
    df = DataFrame({"a": [1, 1, 2], "b": [3, 4, 5]})
    gb = df.groupby("a", as_index=False)["b"]
    result = gb.agg(["sum", "mean"])
    expected = DataFrame({"a": [1, 2], "sum": [7, 5], "mean": [3.5, 5.0]})
    tm.assert_frame_equal(result, expected)

