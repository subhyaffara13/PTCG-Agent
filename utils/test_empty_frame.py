
def test_empty_frame(temp_file):
    # GH 46240
    # create an empty DataFrame with int64 and float64 dtypes
    df = DataFrame(data={"a": range(3), "b": [1.0, 2.0, 3.0]}).head(0)
    path = temp_file
    df.to_stata(path, write_index=False, version=117)
    # Read entire dataframe
    df2 = read_stata(path)
    assert "b" in df2
    # Dtypes don't match since no support for int32
    dtypes = Series({"a": np.dtype("int32"), "b": np.dtype("float64")})
    tm.assert_series_equal(df2.dtypes, dtypes)
    # read one column of empty .dta file
    df3 = read_stata(path, columns=["a"])
    assert "b" not in df3
    tm.assert_series_equal(df3.dtypes, dtypes.loc[["a"]])


def test_empty_frame():
    buf = StringIO()
    df = pd.DataFrame({"id": [], "first_name": [], "last_name": []}).set_index("id")
    df.to_markdown(buf=buf)
    result = buf.getvalue()
    assert result == (
        "| id   | first_name   | last_name   |\n|------|--------------|-------------|"
    )

