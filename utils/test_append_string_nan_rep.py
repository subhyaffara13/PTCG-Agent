
def test_append_string_nan_rep(temp_hdfstore):
    # GH 16300
    df = DataFrame({"A": "a", "B": "foo"}, index=np.arange(10))
    df_nan = df.copy()
    df_nan.loc[0:4, :] = np.nan
    msg = "NaN representation is too large for existing column size"

    # string column too small
    temp_hdfstore.append("sa", df["A"])
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append("sa", df_nan["A"])

    # nan_rep too big
    temp_hdfstore.append("sb", df["B"], nan_rep="bars")
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append("sb", df_nan["B"])

    # smaller modified nan_rep
    temp_hdfstore.append("sc", df["A"], nan_rep="n")
    temp_hdfstore.append("sc", df_nan["A"])
    result = temp_hdfstore["sc"]
    expected = concat([df["A"], df_nan["A"]])
    tm.assert_series_equal(result, expected)

