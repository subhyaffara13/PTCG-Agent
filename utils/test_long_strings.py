
def test_long_strings(temp_hdfstore):
    # GH6166
    data = ["a" * 50] * 10
    df = DataFrame({"a": data}, index=data)

    temp_hdfstore.append("df", df, data_columns=["a"])

    result = temp_hdfstore.select("df")
    tm.assert_frame_equal(df, result)

