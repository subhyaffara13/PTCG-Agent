
def test_agg_index_has_complex_internals(index):
    # GH 31223
    df = DataFrame({"group": [1, 1, 2], "value": [0, 1, 0]}, index=index)
    result = df.groupby("group").agg({"value": Series.nunique})
    expected = DataFrame({"group": [1, 2], "value": [2, 1]}).set_index("group")
    tm.assert_frame_equal(result, expected)

