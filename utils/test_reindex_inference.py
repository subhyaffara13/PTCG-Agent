
def test_reindex_inference():
    # inference of new dtype
    s = Series([True, False, False, True], index=list("abcd"))
    new_index = "agc"
    result = s.reindex(list(new_index)).ffill()
    expected = Series([True, True, False], index=list(new_index), dtype=object)
    tm.assert_series_equal(result, expected)

