
def test_union_keep_dtype_precision(any_real_numeric_dtype):
    # GH#48498
    arr1 = Series([4, 1, 1], dtype=any_real_numeric_dtype)
    arr2 = Series([1, 4], dtype=any_real_numeric_dtype)
    midx = MultiIndex.from_arrays([arr1, [2, 1, 1]], names=["a", None])
    midx2 = MultiIndex.from_arrays([arr2, [1, 2]], names=["a", None])

    result = midx.union(midx2)
    expected = MultiIndex.from_arrays(
        ([Series([1, 1, 4], dtype=any_real_numeric_dtype), [1, 1, 2]]),
        names=["a", None],
    )
    tm.assert_index_equal(result, expected)

