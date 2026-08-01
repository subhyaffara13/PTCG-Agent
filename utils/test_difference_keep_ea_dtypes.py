
def test_difference_keep_ea_dtypes(any_numeric_ea_dtype, val):
    # GH#48606
    midx = MultiIndex.from_arrays(
        [Series([1, 2], dtype=any_numeric_ea_dtype), [2, 1]], names=["a", None]
    )
    midx2 = MultiIndex.from_arrays(
        [Series([1, 2, val], dtype=any_numeric_ea_dtype), [1, 1, 3]]
    )
    result = midx.difference(midx2)
    expected = MultiIndex.from_arrays([Series([1], dtype=any_numeric_ea_dtype), [2]])
    tm.assert_index_equal(result, expected)

    result = midx.difference(midx.sort_values(ascending=False))
    expected = MultiIndex.from_arrays(
        [Series([], dtype=any_numeric_ea_dtype), Series([], dtype=np.int64)],
        names=["a", None],
    )
    tm.assert_index_equal(result, expected)

