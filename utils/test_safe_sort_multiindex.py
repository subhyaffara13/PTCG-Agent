
def test_safe_sort_multiindex():
    # GH#48412
    arr1 = Series([2, 1, NA, NA], dtype="Int64")
    arr2 = [2, 1, 3, 3]
    midx = MultiIndex.from_arrays([arr1, arr2])
    result = safe_sort(midx)
    expected = MultiIndex.from_arrays(
        [Series([1, 2, NA, NA], dtype="Int64"), [1, 2, 3, 3]]
    )
    tm.assert_index_equal(result, expected)

