
def test_empty_df_expanding(expander):
    # GH 15819 Verifies that datetime and integer expanding windows can be
    # applied to empty DataFrames

    expected = DataFrame()
    result = DataFrame().expanding(expander).sum()
    tm.assert_frame_equal(result, expected)

    # Verifies that datetime and integer expanding windows can be applied
    # to empty DataFrames with datetime index
    expected = DataFrame(index=DatetimeIndex([]))
    result = DataFrame(index=DatetimeIndex([])).expanding(expander).sum()
    tm.assert_frame_equal(result, expected)

