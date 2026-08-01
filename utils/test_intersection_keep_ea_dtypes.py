
def test_intersection_keep_ea_dtypes(val, any_numeric_ea_dtype):
    # GH#48604
    midx = MultiIndex.from_arrays(
        [Series([1, 2], dtype=any_numeric_ea_dtype), [2, 1]], names=["a", None]
    )
    midx2 = MultiIndex.from_arrays(
        [Series([1, 2, val], dtype=any_numeric_ea_dtype), [1, 1, 3]]
    )
    result = midx.intersection(midx2)
    expected = MultiIndex.from_arrays([Series([2], dtype=any_numeric_ea_dtype), [1]])
    tm.assert_index_equal(result, expected)

