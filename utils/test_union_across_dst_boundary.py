
def test_union_across_dst_boundary():
    # GH#62915 union should work when one index ends at DST boundary
    # and the other extends past it
    index1 = date_range("2025-10-25", "2025-10-26", freq="D", tz="Europe/Helsinki")
    index2 = date_range("2025-10-25", "2025-10-28", freq="D", tz="Europe/Helsinki")
    result = index1.union(index2)
    expected = date_range("2025-10-25", "2025-10-28", freq="D", tz="Europe/Helsinki")
    tm.assert_index_equal(result, expected)

