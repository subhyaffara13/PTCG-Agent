
def test_column_name_duplicates(names, expected_names, allow_duplicates):
    # GH#44755 reset_index with duplicate column labels
    s = Series([1], index=MultiIndex.from_arrays([[1], [1]], names=names))
    if allow_duplicates:
        result = s.reset_index(allow_duplicates=True)
        expected = DataFrame([[1, 1, 1]], columns=[*expected_names, 0])
        tm.assert_frame_equal(result, expected)
    else:
        with pytest.raises(ValueError, match="cannot insert"):
            s.reset_index()

