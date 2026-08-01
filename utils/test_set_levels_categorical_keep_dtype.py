
def test_set_levels_categorical_keep_dtype():
    # GH#52125
    midx = MultiIndex.from_arrays([[5, 6]])
    result = midx.set_levels(levels=pd.Categorical([1, 2]), level=0)
    expected = MultiIndex.from_arrays([pd.Categorical([1, 2])])
    tm.assert_index_equal(result, expected)

