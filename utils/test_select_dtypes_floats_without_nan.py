
def test_select_dtypes_floats_without_nan(temp_hdfstore):
    df = DataFrame({"cols": range(11), "values": range(11)}, dtype="float64")
    df["cols"] = (df["cols"] + 10).apply(str)

    temp_hdfstore.append("df1", df, data_columns=True)
    result = temp_hdfstore.select("df1", where="values>2.0")
    expected = df[df["values"] > 2.0]
    tm.assert_frame_equal(expected, result)

