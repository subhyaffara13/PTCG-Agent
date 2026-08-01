
def test_setitem_bool_dtype_with_boolean_indexer():
    # GH 57338
    s1 = Series([True, True, True], dtype=bool)
    s2 = Series([False, False, False], dtype=bool)
    condition = [False, True, False]
    s1[condition] = s2[condition]
    expected = Series([True, False, True], dtype=bool)
    tm.assert_series_equal(s1, expected)

