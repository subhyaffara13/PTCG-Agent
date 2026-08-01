
def test_underlying_data_conversion():
    # GH 4080
    df = DataFrame({c: [1, 2, 3] for c in ["a", "b", "c"]})
    return_value = df.set_index(["a", "b", "c"], inplace=True)
    assert return_value is None
    s = Series([1], index=[(2, 2, 2)])
    df["val"] = 0
    df_original = df.copy()
    df

    with tm.raises_chained_assignment_error():
        df["val"].update(s)
    expected = df_original
    tm.assert_frame_equal(df, expected)

