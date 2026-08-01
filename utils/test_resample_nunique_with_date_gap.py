
def test_resample_nunique_with_date_gap(func, unit):
    # GH 13453
    # Since all elements are unique, these should all be the same
    index = date_range("1-1-2000", "2-15-2000", freq="h").as_unit(unit)
    index2 = date_range("4-15-2000", "5-15-2000", freq="h").as_unit(unit)
    index3 = index.append(index2)
    s = Series(range(len(index3)), index=index3, dtype="int64")
    r = s.resample("ME")
    result = r.count()
    expected = func(r)
    tm.assert_series_equal(result, expected)

