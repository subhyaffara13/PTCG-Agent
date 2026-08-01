
def test_groupby_nth_int_like_precision(data):
    # GH#6620, GH#9311
    df = DataFrame({"a": [1, 1], "b": data})

    grouped = df.groupby("a")
    result = grouped.nth(0)
    expected = DataFrame({"a": 1, "b": [data[0]]})

    tm.assert_frame_equal(result, expected)

