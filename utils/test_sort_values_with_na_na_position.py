
def test_sort_values_with_na_na_position(dtype, na_position):
    # 51612
    arrays = [
        Series([1, 1, 2], dtype=dtype),
        Series([1, None, 3], dtype=dtype),
    ]
    index = MultiIndex.from_arrays(arrays)
    result = index.sort_values(na_position=na_position)
    if na_position == "first":
        arrays = [
            Series([1, 1, 2], dtype=dtype),
            Series([None, 1, 3], dtype=dtype),
        ]
    else:
        arrays = [
            Series([1, 1, 2], dtype=dtype),
            Series([1, None, 3], dtype=dtype),
        ]
    expected = MultiIndex.from_arrays(arrays)
    tm.assert_index_equal(result, expected)

