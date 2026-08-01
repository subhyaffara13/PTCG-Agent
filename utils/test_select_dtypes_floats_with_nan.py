
def test_select_dtypes_floats_with_nan(temp_hdfstore):
    df = DataFrame({"cols": range(11), "values": range(11)}, dtype="float64")
    df["cols"] = (df["cols"] + 10).apply(str)
    df.iloc[0] = np.nan
    expected = df[df["values"] > 2.0]

    temp_hdfstore.append("df2", df, data_columns=True, index=False)
    result = temp_hdfstore.select("df2", where="values>2.0")
    tm.assert_frame_equal(expected, result)

