
def test_assert_frame_equal_nested_df_na(na_value):
    # GH#43022
    inner = DataFrame({"a": [1, na_value]})
    df1 = DataFrame({"df": [inner]})
    df2 = DataFrame({"df": [inner]})
    tm.assert_frame_equal(df1, df2)

