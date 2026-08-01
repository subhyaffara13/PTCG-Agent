
def test_union_nan_got_duplicated(dtype, sort):
    # GH#38977, GH#49010
    mi1 = MultiIndex.from_arrays([pd.array([1.0, np.nan], dtype=dtype), [2, 3]])
    mi2 = MultiIndex.from_arrays([pd.array([1.0, np.nan, 3.0], dtype=dtype), [2, 3, 4]])
    result = mi1.union(mi2, sort=sort)
    if sort is None:
        expected = MultiIndex.from_arrays(
            [pd.array([1.0, 3.0, np.nan], dtype=dtype), [2, 4, 3]]
        )
    else:
        expected = mi2
    tm.assert_index_equal(result, expected)

