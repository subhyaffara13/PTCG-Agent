
def test_reindex_pad2():
    # GH4604
    s = Series([1, 2, 3, 4, 5], index=["a", "b", "c", "d", "e"])
    new_index = ["a", "g", "c", "f"]
    expected = Series([1, 1, 3, 3.0], index=new_index)

    # this changes dtype because the ffill happens after
    result = s.reindex(new_index).ffill()
    tm.assert_series_equal(result, expected)

    result = s.reindex(new_index).ffill()
    tm.assert_series_equal(result, expected)

    expected = Series([1, 5, 3, 5], index=new_index)
    result = s.reindex(new_index, method="ffill")
    tm.assert_series_equal(result, expected)

