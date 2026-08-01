
def test_where_inplace_string_array_consistency():
    # GH#46512
    df = DataFrame({"A": ["1", "", "3"]}, dtype="string")
    df_inplace = df.copy()

    result = df.where(df != "", np.nan)
    df_inplace.where(df_inplace != "", np.nan, inplace=True)

    tm.assert_frame_equal(result, df_inplace)

